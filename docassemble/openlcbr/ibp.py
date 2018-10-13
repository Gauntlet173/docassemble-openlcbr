# Adopted from https://github.com/mgrabmair/openlcbr by Matthhias Grabmair

# =============================================================================
# constants
# =============================================================================


ABSTAIN = 'a'
PLAINTIFF = 'p'
DEFENDANT = 'd'

# =============================================================================
# global variables
# =============================================================================
explanation = ""

# =============================================================================
# general model function
# =============================================================================


def issue_raised(case, issue_id, model):
    issue = model['issues'][issue_id]
    if issue['type'] in ['intermediate_issue', 'top_level_issue']:
        return True in map(lambda a: issue_raised(case, a, model), issue['antecedents'])
    elif issue['type'] == 'leaf_issue':
        return len(set(case['factors']) & set(issue['factors'])) > 0
    return None


def issue_factors_in_case(case, issue):
    return set(case['factors']) & set(issue['factors'])


def factors_unanimous_for_side(factor_ids, factor_collection):
    sides = set(map(lambda factor_id: factor_collection[factor_id]['favored_side'], factor_ids))
    if len(sides) == 1:
        return list(sides)[0]
    return False


def cases_unanimous_for_side(cases):
    sides = set(map(lambda c: c['winner'], cases))
    if len(sides) == 1:
        return list(sides)[0]
    return False


def cases_with_factors(factor_ids, cases):
    return list(filter(lambda c: set(factor_ids) <= set(c['factors']), cases))


def case_ko_factors(case, model):
    return set(model['ko_factors']) & set(case['factors'])


def all_plaintiff(predictions):
    return list(set(predictions))[0] == 'p'


def filter_defendant_cases(cases):
    return filter(lambda c: c['winner'] == DEFENDANT, cases)


def filter_plaintiff_factor_ids(factor_ids, all_factors):
    return filter(lambda fid: all_factors[fid]['favored_side']=='p', factor_ids)


# =============================================================================
# prediction model
# =============================================================================


def theory_testing(case, issue, theory_factor_ids, all_factors, cases, model, query_broadened=False):
    global explanation
    issue_precedents = cases_with_factors(theory_factor_ids, cases)

    ## if precedents found do theory testing
    if issue_precedents:
        explanation += "Retrieving cases sharing all factors relevant to issue " + issue['id'] + ": \n\n"
        for c in issue_precedents:
            explanation += '* '+ c['id']+' won by '+c['winner'] + '\n'
        explanation += "\n\n"
        side = cases_unanimous_for_side(issue_precedents)
        ## if cases unanimous predict accordingly
        if side:
            explanation += 'All retrieved cases favour '+side+', predicting issue ' + issue['id'] + ' for ' + side + '.\n\n'
            return side
        else:
            ## if cases not unanimous explain away exceptions using KO factors
            explanation += 'Retrieved cases are not unanimous. Considering knock-out factors.\n\n'
            all_explained_away = True
            for c in filter_defendant_cases(issue_precedents):
                explanation += 'Considering knock-out factors in '+c['id']+ '.\n\n'
                unshared_ko_factors = case_ko_factors(c, model) - set(case['factors'])
                if unshared_ko_factors:
                    explanation += c['id'] \
                          +' was found for the Defendant, but can be distinguished because does not share knock-out factors with the test case: \n\n '
                    for ukf in unshared_ko_factors:
                        explanation += "* " + all_factors[ukf]['description'] + "\n"
                    explanation += "\n\n"
                else:
                    explanation += c['id']+' has no unshared knock-out factors and cannot be distinguished. Predicting issue ' + issue['id'] + 'for Defendant.\n\n'
                    all_explained_away = False
                    return DEFENDANT
            if all_explained_away:
                explanation += 'All counterexamples can be distinguished. Predicting issue ' + issue['id'] + ' for Plaintiff.\n\n'
                return PLAINTIFF

    ## if no precedents found attempt theory testing with broadened query if not already so
    elif not query_broadened:
        explanation += 'There are no cases sharing all relevant factors for issue. Expanding search.\n\n'
        p_factor_ids = set(filter_plaintiff_factor_ids(theory_factor_ids, all_factors))
        ## iterate over broadened query sets
        broadened_all_plaintiff = True
        for pf_id in p_factor_ids:
            explanation += "Running prediction for relevant factors "
            explanation += ' excluding ' + all_factors[pf_id]['description'] + ".\n\n"
            broadened_tt = theory_testing(case, \
                                          issue, \
                                          [f_id for f_id in p_factor_ids if not f_id == pf_id], \
                                          all_factors, \
                                          cases, \
                                          model, \
                                          query_broadened=True)
            explanation += 'Prediction for this broadened query: '+broadened_tt +'.\n\n'
            if not broadened_tt == PLAINTIFF:
                broadened_all_plaintiff = False
        if broadened_all_plaintiff:
            explanation += 'All broadened queries favor Plaintiff, predicting ' + issue['id'] + ' for Plaintiff.\n\n'
            return PLAINTIFF
        else:
            explanation += 'At least one broadened query favors defendant, abstaining on issue ' + issue['id'] + '.\n\n'
            return ABSTAIN

    # if query already broadened and no precedents are found abstain
    else:
        explanation += 'No precedents found in the case database for this issue. Abstaining.\n\n'
        return ABSTAIN


def predict_intermediate_issue(case, issue_id, all_factors, cases, model):
    global explanation
    issue = model['issues'][issue_id]

    # if issue is not raised predict default winner if available, else abstain
    if not issue_raised(case, issue['id'], model):
        if 'winner_if_unraised' in issue:
            pred = issue['winner_if_unraised']
            explanation += 'Issue ' + issue['id']+' has not been raised, and is deemed won by '+pred + '.\n\n'
            return pred
        else:
            explanation += 'Issue ' +issue['id']+' has not been raised and there is no default winner. Abstaining. \n\n'
            return ABSTAIN

    # if issue is raised then predict its antecedents
    else:
        antecedent_preds = list(map(lambda a: predict_issue(case, a, all_factors, cases, model), \
                                    issue['antecedents']))
        # disjunctive antecedents
        if 'disjoint_antecedents' in issue and issue['disjoint_antecedents']:
            explanation += "Sub-issues of issue " + issue['id'] + " are disjoint (any of).\n\n"
            if PLAINTIFF in antecedent_preds:   # one plaintiff prediction suffices
                explanation += "At least one sub-issue is predicted for the plaintiff, predicting issue " + issue['id'] + " for the plaintiff.\n\n"
                return PLAINTIFF
            elif ABSTAIN in antecedent_preds:   # if one antecedent is an abstain, abstain from whole
                explanation += "No sub-issue is predicted for the plaintiff, at least one sub-issue is abstained. Abstaining on issue " + issue['id'] + ".\n\n"
                return ABSTAIN
            else:
                explanation += "No sub-issue is predicted for the plaintiff, and no sub-issue is abstained. Predicting issue " + issue['id'] + " for the defendant.\n\n"
                return DEFENDANT                # otherwise defendant wins
        # default: conjunctive antecedents
        else:
            explanation += "Sub-issues of issue " + issue['id'] + " are conjoint (all of).\n\n"
            if all_plaintiff(antecedent_preds):  # plaintiff if won all antecedents
                explanation += "All sub-issues are predicted for the Plaintiff.  Predicting issue " + issue['id'] + " for the Plaintiff.\n\n"
                return PLAINTIFF
            elif DEFENDANT in antecedent_preds:  # defendant wins if won one antencedent
                explanation += "At least one sub-issue predicted for the Defendant.  Predicting issue " + issue['id'] + " for the Defendant.\n\n"
                return DEFENDANT
            else:
                explanation += "No sub-issues decided for the defendant, and at least one sub-issue abstained. Abstaining on issue " + issue['id'] + ".\n\n"
                return ABSTAIN                   # else abstain


def predict_leaf_issue(case, issue_id, all_factors, cases, model):
    global explanation
    issue = model['issues'][issue_id]

    ## if issue not raised predict default winner
    if not issue_raised(case, issue['id'], model):
        explanation += 'Issue ' + issue['id'] \
              +' has not been raised. predicting for: ' \
              +issue['winner_if_unraised'] + '\n\n'
        return issue['winner_if_unraised']
    else:
        ## if issue raised and factors unanimously favor one side, predict it
        issue_factor_ids = issue_factors_in_case(case, issue)
        explanation += 'Factors in '+case['id']+' relevant to '+issue['id']+' are:\n\n'
        for fid in issue_factor_ids:
            explanation += "* " + all_factors[fid]['description'] + "\n"
        explanation += '\n\n'
        side = factors_unanimous_for_side(issue_factor_ids, all_factors)
        if side:
            explanation += 'All factors unanimously favor '+side+', predicting ' + issue['id'] + ' for ' + side+'.\n\n'
            return side
        else:
            return theory_testing(case, issue, issue_factor_ids, all_factors, cases, model)


def predict_issue(case, issue_id, factors, cases, model):
    global explanation
    issue = model['issues'][issue_id]
    explanation += 'Predicting '+issue['id']+'.\n\n'

    if issue['type'] in ['intermediate_issue', 'top_level_issue']:
        explanation += "Predicting subissues\n\n"
        return predict_intermediate_issue(case, issue_id, factors, cases, model)
    elif issue['type'] == 'leaf_issue':
        return predict_leaf_issue(case, issue_id, factors, cases, model)
    else:
        raise TypeError('unknown issue type'+issue['type'])


def predict_case(case, top_issue_id, factors, case_collection, model):
    global explanation
    explanation = ""
    
    assert top_issue_id in model['issues'], 'top issue '+top_issue_id+' not in domain model'

    # remove test case from collection if in there
    cases = list(filter(lambda c: not c['id'] == case['id'], case_collection['cases']))
    
    explanation += 'Making a prediction on issue ' + model['issues'][top_issue_id]['id'] + ' for case ' + case['id'] + '\n\n'

    pred = predict_issue(case, top_issue_id, factors, cases, model)

    if pred == ABSTAIN:
        explanation += 'Not confident in the prediction, so abstaining.\n\n'
    else:
        correct = pred == case['winner']
        explanation += 'Prediction for '+case['id']+' on issue ' + model['issues'][top_issue_id]['id'] + ' is: '+pred+ '.\n\n'
        if correct:
            explanation += 'Compared to outcome of actual case, prediction is correct. \n\n'
        else:
            explanation += 'Compared to outcome of actual case, prediction is incorrect. \n\n'
    return explanation
