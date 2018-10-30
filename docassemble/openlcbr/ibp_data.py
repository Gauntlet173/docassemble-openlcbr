from docassemble.base.core import DAObject, DAList, DADict, DASet
from docassemble.base.util import *
from DATree import *
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
    target[str(source.id)]['antecedents'] = set()
    for b in source.branches:
      target[str(source.id)]['antecedents'].add(str(b.id))
    if source.join_type == "disjunctive":
      target[str(source.id)]['disjoint_antecedents'] = True
  else:
    target[str(source.id)]['factors'] = set()
    for f in source.factors:
      target[str(source.id)]['factors'].add(str(f.id))
    
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
      newcase['factors'] = set()
      for f in c.factors:
        newcase['factors'].add(str(f.id))
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
    return yaml.dump(output)
    
  #def read(self, file, *pargs, **kwargs):
    #In here, define the code that it should use to load all of the elements into the data structure.
    #pass
    
  #def write(self, file, *pargs, **kwargs):
    #Here would be the code to output the contents of the data structure to YAML.
    #pass

#class DAIBPCaseCollections(DAList):  
  #def init(self, *pargs, **kwargs):
    #self.name = "case_collections"
    #self.object_type = "DAIBPCaseCollection"
    #return super(DAIBPCaseCollections, self).init(*pargs, **kwargs)

#class DAIBPCaseCollection(DAList):  
  #def init(self, *pargs, **kwargs):
    #self.initializeAttribute('id')
    #self.initializatAttribute('cases',DAIBPCases)
    #return super(DAIBPCaseCollection, self).init(*pargs, **kwargs)

#class DAIBPCases(DAList):
  #def init(self, *pargs, **kwargs):
    #self.name = "cases"
    #self.object_type = "DAIBPCase"
    #return super(DAIBPCases, self).init(*pargs, **kwargs)

class DAIBPCase(DAObject):
  def init(self, *pargs, **kwargs):
    self.initializeAttribute('factors',DAList)
    return super(DAIBPCase, self).init(*pargs, **kwargs)
  
#class DAIBPDomainModel(DAObject):
  #def init(self, *pargs, **kwargs):
    #self.initializeAttribute('ko_factors',DAList)
    #self.initializeAttribute('issues',DAIBPIssues)
    #return super(DAIBPDomainModel, self).init(*pargs, **kwargs)

#class DAIBPIssues(DAObject):
  #def init(self, *pargs, **kwargs):
    #self.name = "issues"
    #self.object_type = "DAIBPIssue"
    #return super(DAIBPIssues, self).init(*pargs, **kwargs)
  
class DAIBPIssue(DATree):
  def init(self, *pargs, **kwargs):
    super(DAIBPIssue, self).init(*pargs, **kwargs)
    self.initializeAttribute('factors',DAList)
    self.branches.object_type = DAIBPIssue

#class DAIBPFactors(DAList):
  #def init(self, *pargs, **kwargs):
    #self.object_type = "DAIBPFactor"
    #return super(DAIBPFactors, self).init(*pargs, **kwargs)

#class DAIBPFactor(DAObject):
  #def init(self, *pargs, **kwargs):
    #return super(DAIBPFactor, self).init(*pargs, **kwargs)


  
  