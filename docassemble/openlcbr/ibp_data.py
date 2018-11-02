from docassemble.base.core import DAObject, DAList, DADict, DASet
from docassemble.base.util import *
from DATree import *
from lcbr_explain import *
import yaml

def export_issues_from_tree(target, source):
  # The target is a dictionary.
  # The source is a DATree structure.
  
  target[str(source.id)] = {}
  target[str(source.id)]['id'] = str(source.id)
  target[str(source.id)]['proposition'] = str(source.text)
  target[str(source.id)]['type'] = str(source.type)
  target[str(source.id)]['winner_if_unraised'] = str(source.default)
  # If the current issue has antecedents, grab 'em.
  if source.branches.there_are_any:
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


  
class DAIBPData(DAObject):
  def init(self, *pargs, **kwargs):
    return super(DAIBPData, self).init(*pargs, **kwargs)
  def load(self, database):
    self.datafile = database.path()
    data_files = []
    data_files.append(database.path())
    self.factors, self.case_collections, self.domain_models = load_dataset(data_files)
    self.factorslist = DADict('factors')
    for f in self.factors:
      id = self.factors[f]['id']
      description = self.factors[f]['description']
      self.factorslist[id] = description
    self.factorslist.there_is_another = False
    
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

  def predict(self, test_case):
    case ={}
    case['id'] = 'your-test-case'
    case['factors'] = set()
    for f in self.factors:
      #log("Checking if " + f + " is true in test case", "info")
      if f in test_case.factors:
        #log("True, adding.", "info")
        case['factors'].add(f)
    p = DATree()
    p = ibp_explain.predict_case(case,
                        'trade_secret_misappropriation',
                        self.factors,
                        self.case_collections['trade_secret_test'],
                        self.domain_models['ibp_original'])
    return p
  
  def get_factor_id_by_proposition(self, prop):
    for f in self.factors:
      if self.factors[f]['proposition'] == prop:
        return self.factors[f]['id']
    
  
class DAIBPCase(DAObject):
  def init(self, *pargs, **kwargs):
    super(DAIBPCase, self).init(*pargs, **kwargs)
    self.initializeAttribute('factors',DADict)
    

class DAIBPIssue(DATree):
  def init(self, *pargs, **kwargs):
    super(DAIBPIssue, self).init(*pargs, **kwargs)
    self.initializeAttribute('factors',DAList)
    self.branches.object_type = DAIBPIssue
  