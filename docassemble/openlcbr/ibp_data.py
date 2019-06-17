from docassemble.base.core import DAObject, DAList, DADict, DASet
from docassemble.base.util import *
from DATree import *
from lcbr_explain import *
import yaml
import copy

def export_issues_from_tree(target, source):
  # The target is a dictionary.
  # The source is a DATree structure.
  
  target[str(source.id)] = {}
  target[str(source.id)]['id'] = str(source.id)
  target[str(source.id)]['proposition'] = str(source.text)
  target[str(source.id)]['type'] = str(source.type)
  target[str(source.id)]['winner_if_unraised'] = str(source.default)
  # If the current issue has antecedents, grab 'em.
  if len(source.branches.elements) <> 0:
    # This uses a different format than the database provided by openlcbr
    target[str(source.id)]['antecedents'] = []
    for b in source.branches:
      target[str(source.id)]['antecedents'].append(str(b.id))
    if source.join_type == "disjunctive":
      target[str(source.id)]['disjoint_antecedents'] = True
  else:
    # This uses a different format than the database provided by openlcbr
    target[str(source.id)]['factors'] = []
    for f in source.factors:
      target[str(source.id)]['factors'].append(str(f.id))
    
  for b in source.branches:
    export_issues_from_tree(target, b)
  
  return None

def word_to_side(word):
  if word == "Defendant":
    return 'd'
  elif word == "Plaintiff":
    return 'p'
  else:
    return '?'

def side_to_word(side):
  if side == 'p':
    return 'Plaintiff'
  elif side == "d":
    return "Defendant"
  else:
    return "?"


  
class DAIBPData(DAObject):
  def init(self, *pargs, **kwargs):
    return super(DAIBPData, self).init(*pargs, **kwargs)
  def load(self, database):
    self.datafile = database.path()
    data_files = []
    data_files.append(database.path())
    self.factors, self.case_collections, self.domain_models = load_dataset(data_files)
    self.initializeAttribute('factorslist', DADict)
    for f in self.factors:
      id = self.factors[f]['id']
      description = self.factors[f]['description']
      self.factorslist[id] = description
    self.factorslist.there_is_another = False
  def load_model_only(self, database):
    self.load(database)
    self.case_collections = {}
    self.case_collections['default'] = {}
    self.case_collections['default']['id'] = 'default'
    self.case_collections['default']['cases'] = []
    
  def dump_cases(self):
    return yaml.dump(self.case_collections,default_flow_style=False)
    
  def output_yaml(self, factors, cases, model):
    # The first step is to generate a basic python structure with no objects for the data
    output = {}
    # Factors
    output['factors'] = {}
    for f in factors:
      output['factors'][str(f.id)] = {}
      output['factors'][str(f.id)]['id'] = str(f.id)
      output['factors'][str(f.id)]['proposition'] = str(f.name)
      output['factors'][str(f.id)]['favored_side'] = word_to_side(str(f.side))
      output['factors'][str(f.id)]['description'] = str(f.long_desc)
    # Cases
    output['case_collections'] = {}
    output['case_collections']['docassemble_openlcbr_output'] = {}
    collection = output['case_collections']['docassemble_openlcbr_output']
    collection['id'] = "docassemble_openlcbr_output"
    collection['cases'] = []
    for c in cases:
      newcase = {}
      newcase['id'] = str(c.id)
      newcase['name'] = str(c.name)
      newcase['year'] = str(c.year)
      newcase['winner'] = word_to_side(str(c.winner))
      newcase['citation'] = str(c.cite)
      # This uses a different format than the database provided by openlcbr
      newcase['factors'] = []
      for f in c.factors:
        newcase['factors'].append(str(f.id))
      collection['cases'].append(newcase)
    # Domain Models
    output['domain_models'] = {}
    output['domain_models']['docassemble_openlcbr_output'] = {}
    output['domain_models']['docassemble_openlcbr_output']['id'] = 'docassemble_openlcbr_output'
    output['domain_models']['docassemble_openlcbr_output']['ko_factors'] = []
    kofactors = output['domain_models']['docassemble_openlcbr_output']['ko_factors']
    for kof in model.ko_factors:
      kofactors.append(str(kof.id))
    output['domain_models']['docassemble_openlcbr_output']['issues'] = {}
    issues = output['domain_models']['docassemble_openlcbr_output']['issues'] = {}
    if model.issues.build:
      export_issues_from_tree(issues, model.issues)
    
    #The second step is to spit it out in yaml.
    return yaml.dump(output,default_flow_style=False)

  def predict(self, test_case, case_collection='docassemble_openlcbr_output', model="docassemble_openlcbr_output", issue="trade_secret_misappropriation"):
    case ={}
    case['id'] = 'your-test-case'
    case['factors'] = set()
    for f in self.factors:
      if f in test_case.factors:
        case['factors'].add(f)
    p = DATree()
    p = ibp_explain.predict_case(case,
                        issue,
                        self.factors,
                        self.case_collections[case_collection],
                        self.domain_models[model])
    return p
  
  def get_factor_id_by_proposition(self, prop):
    for f in self.factors:
      if self.factors[f]['proposition'] == prop:
        return self.factors[f]['id']
      
  def add_precedent_case(self, case):
    # This will be used once for each case to be added
    default_cases = self.case_collections['default']['cases']
    #Create a new case with id, winner, factors.
    newcase = {}
    newcase['id'] = str(case.id)
    if case.winner:
      newcase['winner'] = word_to_side(str(case.winner))
    newcase['factors'] = []
    for f in case.factors:
      newcase['factors'].append(f)
    default_cases.append(newcase)

  def get_predictive_strength(self, case_collection="docassemble_openlcbr_output", model="docassemble_openlcbr_output"):
    # Get a leave-one-out test score for the reasoner.

    correct_predictions = 0.0
    total_predictions = 0.0
    top_issue = ""

    # Get the root issue
    for i in self.domain_models[model]['issues']:
      if self.domain_models[model]['issues'][i]['type'] == "top":
        top_issue = self.domain_models[model]['issues'][i]['id']
        break


    # For Each Case in the Database
    for c in self.case_collections[case_collection]['cases']:
      
      # Create a new reasoner
      temp_reasoner = DAIBPData()
       
      # Give it the same Data
      temp_reasoner.factors = self.factors
      temp_reasoner.domain_models = self.domain_models
      temp_reasoner.case_collections = copy.deepcopy(self.case_collections)

      # Remove the case to be tested from the relevant case database
      temp_reasoner.case_collections[case_collection]['cases'].remove(c)

      # Make a DAIBPCase out of the current case data:
      temp_test_case = DAIBPCase()
      for f in c['factors']:
        temp_test_case.factors.append(f)
      temp_test_case.factors.gathered = True
      
      # Predict that Case against the remainder, Record the Result
      #log("Predicting case " + c['id'] +", actual result " + c['winner'], "info")
      result = temp_reasoner.predict(temp_test_case, case_collection, model, top_issue)
      #log("Prediction is " + result.prediction, "info")
      if result.prediction == c['winner']:
        correct_predictions += 1
      total_predictions += 1
      #log("So far, " + str(correct_predictions) + " correct predictions out of " + str(total_predictions), "info")
      
    # Tell the user what percentage of cases were correctly predicted.
    return (correct_predictions/total_predictions)*100.0

  def get_all_predictions(self, case_collection="docassemble_openlcbr_output", model="docassemble_openlcbr_output"):
    # Get a leave-one-out test score for the reasoner.

    top_issue = ""
    output = DATree()
    output.text = "All Leave-One-Out Predictions"

    # Get the root issue
    for i in self.domain_models[model]['issues']:
      if self.domain_models[model]['issues'][i]['type'] == "top":
        top_issue = self.domain_models[model]['issues'][i]['id']
        break


    # For Each Case in the Database
    for c in self.case_collections[case_collection]['cases']:
      new_case_output = DATree()
      new_case_output.text = str(c)

      # Create a new reasoner
      temp_reasoner = DAIBPData()
       
      # Give it the same Data
      temp_reasoner.factors = self.factors
      temp_reasoner.domain_models = self.domain_models
      temp_reasoner.case_collections = copy.deepcopy(self.case_collections)

      # Remove the case to be tested from the relevant case database
      temp_reasoner.case_collections[case_collection]['cases'].remove(c)

      # Make a DAIBPCase out of the current case data:
      temp_test_case = DAIBPCase()
      
      for f in c['factors']:
        temp_test_case.factors.append(f)
      temp_test_case.factors.gathered = True
      
      # Predict that Case against the remainder, Record the Result
      result = temp_reasoner.predict(temp_test_case, case_collection, model, top_issue)
      
      new_case_output.branches.append(result)
      new_case_output.branches.gathered = True
      
      output.branches.append(new_case_output)
    output.branches.gathered = True  
    return output
  
class DAIBPCase(DAObject):
  def init(self, *pargs, **kwargs):
    super(DAIBPCase, self).init(*pargs, **kwargs)
    self.initializeAttribute('factors',DAList.using(object_type=DAObject))
    

class DAIBPIssue(DATree):
  def init(self, *pargs, **kwargs):
    super(DAIBPIssue, self).init(*pargs, **kwargs)
    self.initializeAttribute('factors',DAList)
    self.branches.object_type = DAIBPIssue
  def iterator(self):
    # Returns a list of the elements in the tree below this object.
    output = []
    output.append(self)
    for b in self.branches:
      output.extend(b.iterator())
    return output

def import_yaml_to_DA(database, factors, cases, model, case_collection='docassemble_openlcbr_output', domain_model='docassemble_openlcbr_output'):
  # First, take the content of the yaml file and turn it into Python data.
  stream = open(database, 'r')
  data = yaml.load(stream)
  
  new_factors = {}
  # Load the Factors into the factors object
  for f in data['factors']:
    #new_factor = DAObject()
    new_factor = factors.appendObject()
    new_factor.id = f
    new_factor.side = side_to_word(data['factors'][f]['favored_side'])
    new_factor.long_desc = data['factors'][f]['description']
    new_factor.name = data['factors'][f]['proposition']
    #factors.append(new_factor.copy_shallow('factors'))
    new_factors[f] = new_factor
  factors.gathered = True
  #factors.auto_gather = False 

  # Load the Cases into the Cases Object
  for c in data['case_collections'][case_collection]['cases']:
    #new_case = DAIBPCase()
    new_case = cases.appendObject(DAIBPCase)
    new_case.id = c['id']
    if 'name' in c:
      new_case.name = c['name']
    else:
      new_case.name = c['citation']
    new_case.year = c['year']
    new_case.cite = c['citation']
    new_case.winner = side_to_word(c['winner'])
    for f in c['factors']:
      #new_case.factors.append(new_factors[f].copy_shallow('factors'))
      for factor in factors:
        if factor.id == f:
          # See notes below about adding factors to issues. Bug.
          new_case.factors.append(factor)
          break
    new_case.factors.gathered = True
    #new_case.factors.auto_gather = False
    #cases.append(new_case)
  cases.gathered = True
  #cases.auto_gather = False

  # Load the model into the model Object
  new_issues = {} # So that we can come back to it and use it to add branches.
  top_issue = None # To keep track of which issue is the root issue.
  issues = data['domain_models'][domain_model]['issues']
  for i in issues:
    new_issue = DAIBPIssue()
    new_issue.initializeAttribute('factors', DAList)
    new_issue.initializeAttribute('branches', DAList)
    new_issue.id = issues[i]['id']
    new_issue.text = issues[i]['proposition']
    new_issue.type = issues[i]['type']
    if new_issue.type == "top" or new_issue.type == "top_level_issue":
      top_issue = new_issue
    if 'winner_if_unraised' in issues[i]:
      new_issue.default = issues[i]['winner_if_unraised']
    if 'antecedents' in issues[i]:
      if 'disjoint_antecedents' in issues[i]:
        new_issue.join_type = "disjunctive"
      else:
        new_issue.join_type = "conjunctive"
    
    
    new_issue.factors.gathered = True
    #new_issue.factors.auto_gather = False
    new_issue.complete = True
    new_issue.branches.gathered = True
    new_issue.branches.object_type = DAIBPIssue
    #new_issue.branches.auto_gather = False
    new_issues[i] = new_issue
  
  # Do the recursive naming prior to adding factors and antecedents.
  top_issue._set_instance_name_recursively('model.issues')
  
  for i in issues:
    if 'factors' in issues[i]:
      for f in issues[i]['factors']:
        for factor in factors:
          if factor.id == f:
            new_issues[i].factors.append(factor)
            break
    if 'antecedents' in issues[i]:
      for a in issues[i]['antecedents']:
        new_issues[i].branches.append(new_issues[a])
        
  model.ko_factors = DAList('model.ko_factors')
  for kof in data['domain_models'][domain_model]['ko_factors']:
    for factor in factors:
      if factor.id == kof:
        model.ko_factors.append(factor)
  model.ko_factors.gathered = True
  #model.ko_factors.auto_gather = False
  model.issues = top_issue
  model.issues.build = True
  #model.issues._set_instance_name_recursively('model.issues')
    