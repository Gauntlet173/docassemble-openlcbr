# Adopted from https://github.com/mgrabmair/openlcbr by Matthhias Grabmair

import sys
import os
import yaml
from docassemble.base.util import *
import ibp


## =============================================================================
## Loading
## =============================================================================


def parse_args():
    if len(sys.argv) < 2:
        print("missing yaml files as command line arguments")
        sys.exit(2)
    else:
        files = sys.argv[1:]
        for f in files:
            if not os.path.isfile(f):
                print("cannot find argument file path: " + f)
                sys.exit(2)
    return files


def load_dataset(data_files):
    factors = {}
    case_collections = {}
    domain_models = {}

    for f in data_files:
        with open(f, 'r') as stream:
            #print('loading: '+f)
            try:
                data = yaml.load(stream)
                if 'factors' in data:
                    factors = data['factors']
                if 'domain_models' in data:
                    domain_models = data['domain_models']
                if 'case_collections' in data:
                    case_collections = data['case_collections']
            except yaml.YAMLError as exc:
                log('error loading data from yaml files',"info")
                log(exc, "info")
    return factors, case_collections, domain_models


def case_from_collection(case_id, case_collection):
    found = list(filter(lambda c: c['id'] == case_id,
                        case_collection['cases']))
    assert len(found) > 0, 'target case '+case_id+' not found in '+case_collection['id']
    assert len(found) == 1, 'multiple cases with id '+case_id+' found in '+case_collection['id']
    return found[0]


## =============================================================================
## main script
## =============================================================================

## currently this is just a test for the model prediction in the KG case as published in:
## Brueninghaus, Stefanie, and Kevin D. Ashley. "Combining case-based and model-based reasoning for predicting the outcome of legal cases." In International Conference on Case-Based Reasoning, pp. 65-79. Springer, Berlin, Heidelberg, 2003.
## https://pdfs.semanticscholar.org/24a4/7ca6f5b2ebec9e809bf19d2b0f0da3dcab81.pdf
## Note: The example in this version uses a slightly different domain model due to being a code migration from VJAP. One modification is that F14 and F25 are associated with improper means which is consistent with IBP domain model diagrams but inconsistent with the KG prediction trace in the referenced paper


#if __name__ == '__main__':
def run_lcbr_test(file):
    try:
        #print("== open ibp test ==")
        # for this implementation I want it to take the file name from the sources folder of the docassemble package
        #data_files = parse_args()
        data_files = [file]
        factors, case_collections, domain_models = load_dataset(data_files)
        case = case_from_collection('KG', case_collections['trade_secret_test'])
        p = ibp.predict_case(case,
                         'trade_secret_misappropriation',
                         factors,
                         case_collections['trade_secret_test'],
                         domain_models['ibp_original'])
        return p
    except Exception as e:
        log(e, "info")