# =============================================================================
# constants
# =============================================================================


ABSTAIN = 'a'
PLAINTIFF = 'p'
DEFENDANT = 'd'


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
    sides = set(map(lambda factor_id: factor_collection[factor_id]['favored_side'],
                    factor_ids))
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

    issue_precedents = cases_with_factors(theory_factor_ids, cases)

    ## if precedents found do theory testing
    if issue_precedents:
        print("retrieved cases sharing "+str(theory_factor_ids))
        for c in issue_precedents:
            print(c['id']+' '+str(set(c['factors']))+' won by '+c['winner'])
        side = cases_unanimous_for_side(issue_precedents)
        ## if cases unanimous predict accordingly
        if side:
            print('cases unanimously favor '+side)
            return side
        else:
            ## if cases not unanimous explain away exceptions using KO factors
            print('cases not unanimous, trying to explain away')
            all_explained_away = True
            for c in filter_defendant_cases(issue_precedents):
                print('trying to explain away '+c['id'])
                unshared_ko_factors = case_ko_factors(c, model) - set(case['factors'])
                if unshared_ko_factors:
                    print(c['id']
                          +' can be explained away by unshared KO factors '
                          +str(unshared_ko_factors))
                else:
                    print(c['id']+' has no unshared KO factors; cannot be explained away')
                    all_explained_away = False
                    return DEFENDANT
            if all_explained_away:
                print('all counterexamples can be explained away')
                return PLAINTIFF

    ## if no precedents found attempt theory testing with broadened query if not already so
    elif not query_broadened:
        print('no cases retrieved in theory testing, broadening query')
        p_factor_ids = set(filter_plaintiff_factor_ids(theory_factor_ids, all_factors))
        print('each of '+str(p_factor_ids)+' is dropped for new theory testing')
        ## iterate over broadened query sets
        broadened_all_plaintiff = True
        for pf_id in p_factor_ids:
            broadened_tt = theory_testing(case,
                                          issue,
                                          [f_id for f_id in p_factor_ids if not f_id == pf_id],
                                          all_factors,
                                          cases,
                                          model,
                                          query_broadened=True)
            print('prediction for this broadened query: '+broadened_tt)
            if not broadened_tt == PLAINTIFF:
                broadened_all_plaintiff = False
        if broadened_all_plaintiff:
            print('all broadened queries favor plaintiff')
            return PLAINTIFF
        else:
            print('at least one broadened query favors defendant')
            return ABSTAIN

    # if query already broadened and no precedents are found abstain
    else:
        print('no precedents found. abstaining')
        return ABSTAIN


def predict_intermediate_issue(case, issue_id, all_factors, cases, model):

    issue = model['issues'][issue_id]

    # if issue is not raised predict default winner if available, else abstain
    if not issue_raised(case, issue['id'], model):
        if 'winner_if_unraised' in issue:
            pred = issue['winner_if_unraised']
            print(issue['id']+' is has not been raised and is deemed won by '+pred)
            return pred
        else:
            print(issue['id']+' is has not been raised and there is no default winner. abstaining')
            return ABSTAIN

    # if issue is raised then predict its antecedents
    else:
        antecedent_preds = list(map(lambda a: predict_issue(case, a, all_factors, cases, model),
                                    issue['antecedents']))
        # disjunctive antecedents
        if 'disjoint_antecedents' in issue and issue['disjoint_antecedents']:
            if PLAINTIFF in antecedent_preds:   # one plaintiff prediction suffices
                return PLAINTIFF
            elif ABSTAIN in antecedent_preds:   # if one antecedent is an abstain, abstain from whole
                return ABSTAIN
            else:
                return DEFENDANT                # otherwise defendant wins
        # default: conjunctive antecedents
        else:
            if all_plaintiff(antecedent_preds):  # plaintiff if won all antecedents
                return PLAINTIFF
            elif DEFENDANT in antecedent_preds:  # defendant wins if won one antencedent
                return DEFENDANT
            else:
                return ABSTAIN                   # else abstain


def predict_leaf_issue(case, issue_id, all_factors, cases, model):

    issue = model['issues'][issue_id]

    ## if issue not raised predict default winner
    if not issue_raised(case, issue['id'], model):
        print(issue['id']
              +' has not been raised. predicting for: '
              +issue['winner_if_unraised'])
        return issue['winner_if_unraised']
    else:
        ## if issue raised and factors unanimously favor one side, predict it
        issue_factor_ids = issue_factors_in_case(case, issue)
        print('factors in '+case['id']+' for '+issue['id']+': '+str(issue_factor_ids))
        side = factors_unanimous_for_side(issue_factor_ids, all_factors)
        if side:
            print('all factors unanimously favor '+side)
            return side
        else:
            return theory_testing(case, issue, issue_factor_ids, all_factors, cases, model)


def predict_issue(case, issue_id, factors, cases, model):

    issue = model['issues'][issue_id]
    print('Analyzing case '+case['id'])
    print('predicting '+issue['id'])

    if issue['type'] in ['intermediate_issue', 'top_level_issue']:
        return predict_intermediate_issue(case, issue_id, factors, cases, model)
    elif issue['type'] == 'leaf_issue':
        return predict_leaf_issue(case, issue_id, factors, cases, model)
    else:
        raise TypeError('unknown issue type'+issue['type'])


def predict_case(case, top_issue_id, factors, case_collection, model):

    assert top_issue_id in model['issues'], 'top issue '+top_issue_id+' not in domain model'

    # remove test case from collection if in there
    cases = list(filter(lambda c: not c['id'] == case['id'], case_collection['cases']))

    pred = predict_issue(case, top_issue_id, factors, cases, model)

    if pred == ABSTAIN:
        print('system is abstaining from prediction')
    else:
        correct = pred == case['winner']
        print('prediction for '+case['id']+': '+pred)
        if correct:
            print('which is CORRECT')
        else:
            print('which is INCORRECT')
