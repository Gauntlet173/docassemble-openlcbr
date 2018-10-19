from DATree import *
from docassemble.base.util import *

# Adopted from https://github.com/mgrabmair/openlcbr by Matthhias Grabmair

# =============================================================================
# constants
# =============================================================================
ABSTAIN = 'a'
PLAINTIFF = 'p'
DEFENDANT = 'd'

# =============================================================================
# general model function
# =============================================================================

def prediction_word(prediction):
  if prediction == "p":
    return "plaintiff"
  elif prediction == "d":
    return "defendant"
  elif prediction == "a":
    return "abstain"

def issue_factors_in_case(case, issue):
    return set(case['factors']) & set(issue['factors'])


def cases_with_factors(factor_ids, cases):
    return list(filter(lambda c: set(factor_ids) <= set(c['factors']), cases))


def case_ko_factors(case, model):
    return set(model['ko_factors']) & set(case['factors'])


def filter_defendant_cases(cases):
    return filter(lambda c: c['winner'] == DEFENDANT, cases)


def filter_plaintiff_factor_ids(factor_ids, all_factors):
    return filter(lambda fid: all_factors[fid]['favored_side']=='p', factor_ids)


# =============================================================================
# prediction model
# =============================================================================


def predict_case(case, top_issue_id, factors, case_collection, model):
    #log("Predicting a case. We got this far.", "info")
    explanation = DATree('explanation')
    
    
    assert top_issue_id in model['issues'], 'top issue '+top_issue_id+' not in domain model'

    # remove test case from collection if in there
    cases = list(filter(lambda c: not c['id'] == case['id'], case_collection['cases']))
    
    explanation = predict_issue(case, top_issue_id, factors, cases, model)
    
    return explanation

  

def predict_issue(case, issue_id, factors, cases, model):
  #log("Predicting issue " + issue_id, "info")
  explanation = DATree('predict_issue_explanation')
  issue = model['issues'][issue_id]
  
  #    if it's a leaf issue, predict it, and return the prediction.
  if issue['type'] == "leaf_issue":
    #log("Before leaf issue predict", "info")
    explanation = predict_leaf_issue(case, issue_id, factors, cases, model)
    #log("After leaf issue predict", "info")
    return explanation
  #    if it's an interim issue or a root issue
  else:
    #      for each sub-issue
    for subissue in issue['antecedents']:
      #        create a sub-node
      #        set the value of that sub-node to the prediction for the subissue by calling predict issue.
      subexplanation = DATree('subexplanation')
      subexplanation = predict_issue(case, subissue, factors, cases, model)
      explanation.branches.append(subexplanation)      

    # Gather Stats about sub-issues, determine if issue was raised.
    explanation.raised = False
    branch_count, plaintiff_subissues, defendant_subissues, abstain_subissues = 0, 0, 0, 0
    for branch in explanation.branches:
      branch_count = branch_count+1
      if branch.raised:
        explanation.raised = True
      if branch.prediction == PLAINTIFF:
        plaintiff_subissues = plaintiff_subissues+1
      if branch.prediction == DEFENDANT:
        defendant_subissues = defendant_subissues+1
      if branch.prediction == ABSTAIN:
        abstain_subissues = abstain_subissues+1
    
    # If this issue is not raised
    if explanation.raised == False:
      # If it has a default
      if 'winner_if_unraised' in issue:
        # Predict the default
        explanation.prediction = issue['winner_if_unraised']
        explanation.text = "The issue of whether it is true that " + model['issues'][issue_id]['proposition'] \
          + " was not raised in the test case, and can be predicted for the " \
          + prediction_word(explanation.prediction) + " by default."
      else:
        # otherwise, abstain
        explanation.prediction = ABSTAIN
        explanation.text = "The issue of whether it is true that " + model['issues'][issue_id]['proposition'] \
          + " was not raised in the test case, and cannot be predicted."
      return explanation
    
    # combine the prediction values to predict this issue (conjunctive or disjunctive)
    if 'disjoint_antecedents' in issue and issue['disjoint_antecedents']: # I don't understand this style.
      #if at least one branch predicts for plaintiff, predict for plaintiff.
      if plaintiff_subissues > 0:
        explanation.prediction = PLAINTIFF
        explanation.text = "It is true that " + model['issues'][issue_id]['proposition'] \
          + ", as at least one of the requirements for that finding is met."
      elif abstain_subissues > 0:
        explanation.prediction = ABSTAIN
        explanation.text = "I cannot determine whether it is true that " + model['issues'][issue_id]['proposition'] \
          + ", as I do not know whether at least one of the requirements for that finding would be met."
      else:
        explanation.prediction = DEFENDANT
        explanation.text = "It is not true that " + model['issues'][issue_id]['proposition'] \
          + ", as none one of the requirements for that finding are met."
    else: #antecedents are conjoint
      if plaintiff_subissues == branch_count:
        explanation.text = "It is true that " + model['issues'][issue_id]['proposition'] \
          + ", as all of the requirements for that finding are met."
        explanation.prediction = PLAINTIFF
      elif defendant_subissues > 0:
        explanation.text = "It is not true that " + model['issues'][issue_id]['proposition'] \
          + ", as not all of the requirements for that finding are met."
        explanation.prediction = DEFENDANT
      else:
        explanation.text = "I cannot determine whether it is true that " + model['issues'][issue_id]['proposition'] \
          + ", as I do not know whether all of the requirements for that finding would be met."
        explanation.prediction = ABSTAIN
        
    # return the combined prediction for this node
    return explanation

  

#  Predict Leaf Issue (details)
def predict_leaf_issue(case, issue_id, factors, cases, model):
  #log("Predicting leaf issue " + issue_id, "info")
  #Create a node object to return
  explanation = DATree('predicting_leaf_issue_explanation')
  issue = model['issues'][issue_id]
  
  # See if the issue was raised
  #log("Checking raised.", "info")
  explanation.raised = len(set(case['factors']) & set(issue['factors'])) > 0
  
  if not explanation.raised: #this is not the same format he used in the other one
    if 'winner_if_unraised' in issue:
      explanation.prediction = issue['winner-if-unraised']
      explanation.text = "The issue of whether it is true the " + issue['proposition'] + " was not raised " \
        + "in the test case, and can be presumed to " \
        + "be found in favour of the " + prediction_word(explanation.prediction) + "."
    else:
      explanation.prediction = ABSTAIN
      explanation.text = "The issue of whether it is true the " + issue['proposition'] + " was not raised in the test case."
    return explanation
  
  #log("Checking unanimity.", "info")
  factor_unanimity_explanation = DATree('factor_unanimity_explanation')
  factor_unanimity_explanation = predict_leaf_issue_by_factor_unanimity(case, factors)
  explanation.branches.append(factor_unanimity_explanation)
  if factor_unanimity_explanation.prediction != ABSTAIN:
    explanation.prediction = unanimity_explanation.prediction
    explanation.text = "All of the relevant factors with regard to whether it is true that " \
      + "the " + issue['proposition'] + " favour the  " + prediction_word(explanation.prediction) + "."
    return explanation
  
  #log("Checking theory.", "info")
  theory_explanation = DATree('theory_explanation')
  theory_explanation = predict_leaf_by_theory(case, issue_id, issue_factors_in_case(case, issue), factors, cases, model)
  explanation.branches.append(theory_explanation)
  explanation.prediction = theory_explanation.prediction
  if explanation.prediction == ABSTAIN:
    explanation.text = "A review of the relevant cases is inconclusive with regard to whether it is true that " \
      + "the " + issue['proposition'] + "."
  else:
    explanation.text = "A review of the relevant cases shows the issue of whether it is true that the " \
      + issue['proposition'] + " would be decided for the " \
      + prediction_word(explanation.prediction) + "."
  return explanation

def predict_leaf_by_theory(case, issue_id, theory_factors, factors, cases, model, broadened_query = False):
  #log("Predicting leaf issue by theory ", "info")
  explanation = DATree('predict_leaf_by_theory_explanation')
  issue = model['issues'][issue_id]
  relevant_cases = cases_with_factors(theory_factors, cases)
  ko_factors = model['ko_factors']
  
  #log("generating relevant factors list", "info")
  if not broadened_query:
    relevant_factors_list = DATree('relevant_factors_list')
    relevant_factors_list.text = "The factors in the test case relevant to the issue are:"
    for f in theory_factors:
      factor_entry = DATree('factor_entry')
      factor_entry.text = "Whether the " + factors[f]['description'] + "."
      relevant_factors_list.branches.append(factor_entry)
    explanation.branches.append(relevant_factors_list)
  
  #log("generating relevant cases list", "info")
  p_cases, d_cases, case_count = 0, 0, 0
  if relevant_cases: #does this work?
    relevant_cases_list = DATree('relevant_cases_list')
    relevant_cases_list.text = "The cases sharing all of these factors with the test case are:"
    for c in relevant_cases:
      case_count = case_count+1
      case_entry = DATree('case_entry')
      case_entry.text = c['id'] + ", which was decided for the " + prediction_word(c['winner']) + "."
      relevant_cases_list.branches.append(case_entry)
      if c['winner'] == PLAINTIFF:
        p_cases = p_cases+1
      if c['winner'] == DEFENDANT:
        d_cases = d_cases+1
    explanation.branches.append(relevant_cases_list)
  else:
    no_relevant_cases = DATree('no_relevant_cases')
    no_relevant_cases.text = "There are no cases sharing all of these factors with the test case."
    explanation.branches.append(no_relevant_cases)
    
  #log("checking for unanimous cases", "info")
  if relevant_cases:
    if p_cases == case_count:
      explanation.prediction = PLAINTIFF
      explanation.text = "All of the relevant cases were found for the plaintiff."
      return explanation
    elif d_cases == case_count:
      explanation.prediction = DEFENDANT
      explanation.text = "All of the relevant cases were found for the defendant."
      return explanation
    else: #attempt knockouts
      #log("attempting knockouts", "info")
      
      
      ko_factor_list = DATree('ko_factor_list')
      ko_factor_list.text = "The following factors may be used to distinguish cases from one another:"
      for kof in ko_factors:
        ko_factor_entry = DATree('ko_factor_entry')
        ko_factor_entry.text = "Whether the " + factors[kof]['description'] + "."
        ko_factor_list.branches.append(ko_factor_entry)
      explanation.branches.append(ko_factor_list)
      
      all_explained_away = True
      for c in filter_defendant_cases(relevant_cases):
        ko_attempt_entry = DATree('ko_attempt_entry')
        explanation.branches.append(ko_attempt_entry)
        unshared_ko_factors = case_ko_factors(c, model) - set(case['factors'])
        if unshared_ko_factors:
          #log("UKF: " + str(unshared_ko_factors), "info")
          ukf_list = DATree('ukf_list')
          ukf_list.text = "The distinguishing factors not common between the test case and " + c['id'] + " include:"
          ko_attempt_entry.text = "The case " + c['id'] + " can be distinguished from the test case."
          ko_attempt_entry.branches.append(ukf_list)
          for ukf in unshared_ko_factors:
            ukf_entry = DATree('ukf_entry')
            ukf_entry.text = "Whether the " + factors[ukf]['description'] + "."
            ukf_list.branches.append(ukf_entry)
        else:
          ko_attempt_entry.text = "The case " + c['id'] + " cannot be distinguished from the test case."
          all_explained_away = False
        
      if all_explained_away:
        explanation.text = "All the cases similar to the test case with regard to the most important factors were found " \
          + "for the plaintiff. All cases found for the defendant can be distinguished from the test case."
        explanation.prediction = PLAINTIFF
      else:
        explanation.text = "At least one case which is similar to the test case with regard to the most important factors " \
          + "was decided in favour of the defendant."
        explanation.prediction = DEFENDANT
      return explanation
    
  if not broadened_query:
    #log("Attempting broad search", "info")
    relevant_p_factors = set(filter_plaintiff_factor_ids(theory_factors, factors))
    ## iterate over broadened query sets
    broadened_all_plaintiff = True
    for pf_id in relevant_p_factors:
      broad_entry = DATree('broad_entry')
      broad_entry.text = "Considering cases that share all relevant factors except whether the " + factors[pf_id]['description'] + "."
      broad_result = DATree('broad_result')
      broad_result = predict_leaf_by_theory(case,
                                            issue_id,
                                            [f_id for f_id in relevant_p_factors if not f_id == pf_id],
                                            factors,
                                            cases,
                                            model,
                                            broadened_query=True)
      if not broad_result.prediction == PLAINTIFF:
        broadened_all_plaintiff = False
      broad_entry.branches.append(broad_result)
      explanation.branches.append(broad_entry) 
    if broadened_all_plaintiff:
      explanation.prediction = PLAINTIFF
      explanation.text = "There are no cases that share all of the relevant factors with the test case. However,"\
        + " all of the broadened case searches would be predicted for the plaintiff."
    else:
      explanation.prediction = ABSTAIN
      explanation.text = "There are no cases that share all of the relevant factors with the test case, and"\
        + " not all of the broadened case searches would be predicted for the plaintiff."
    
    return explanation

  # if you got to here, there are no cases, and the query is already broadened
  if not relevant_cases and broadened_query:
    #log("Abstaining because broad and no cases", "info")
    explanation.text = "There are no relevant cases in the database."
    explanation.prediction = ABSTAIN
    return explanation
    

def predict_leaf_issue_by_factor_unanimity(case, factors):
  #log("Predicting issue by factor unanimity", "info")
  explanation = DATree('predict_leaf_issue_by_factor_unanimity_explanation')
  
  # Get the way the factors lean
  #log("Setting variables", "info")
  case_factor_count, plaintiff_factors, defendant_factors = 0, 0, 0
  for factor in case['factors']:
    #log("Checking factor " + factor, "info")
    factor_description = DATree('factor_description')
    factor_description.text = "The factor of whether the " + factors[factor]['description'] + " favours the " + prediction_word(factors[factor]['favored_side']) + "."
    explanation.branches.append(factor_description)
    case_factor_count = case_factor_count+1
    if factors[factor]['favored_side'] == PLAINTIFF:
      plaintiff_factors = plaintiff_factors+1
    if factors[factor]['favored_side'] == DEFENDANT:
      defendant_factors = defendant_factors+1
  
  #log("Results P: " + str(plaintiff_factors) + " D: " + str(defendant_factors) + " All: " + str(case_factor_count), "info")
  # if unanimous factors, return that result
  if plaintiff_factors == case_factor_count:
    explanation.text = "This issue can be predicted for the plaintiff, because all the factors present favour the plaintiff."
    explanation.prediction = PLAINTIFF
  elif defendant_factors == case_factor_count:
    explanation.text = "This issue can be predicted for the defendant, because all the factors present favour the defendant."
    explanation.prediction = DEFENDANT
  else:
    explanation.text = "This issue cannot be predicted based soley on the factors, because there are factors favouring both the plaintiff and the defendant."
    explanation.prediction = ABSTAIN
  return explanation



