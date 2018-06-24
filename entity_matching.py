

import sys
import json
import traceback
from log import log_
from entity_matching_api import *
from parameters import *
def entity_matching(sysargv):
    parameters = json.loads(sysargv)

    # This script will be called once a user call made.
    # parameters should be a json stream like:
    #  {
    # "match_source":[{},{}],
    # "match_list":[{},{}],
    # "match_source_category":"...",
    # "match_list_category":"...",
    # "match_source_fields":[],
    # "match_list_fields":[]
    # }
    #test = {'test':'test','t':0}

    #print(test)

    match_source = (parameters['match_source'])
    match_list = list(parameters['match_list'])
    match_source_category = parameters['match_source_category']
    match_list_category = parameters['match_list_category']
    match_source_fields = list(parameters['match_source_fields'])
    match_list_fields = list(parameters['match_list_fields'])

    print( entity_matching_api(match_source,match_list,match_source_category,match_list_category,match_source_fields,match_list_fields,algorithm="wup_similarity"))

if len(sys.argv)>1:
    if version_general=="dev":
        entity_matching(sys.argv[1])
    else:
        try:
            entity_matching(sys.argv[1])
        except Exception:
            try:
                exc_info = sys.exc_info()
            finally:
                formatted_lines = traceback.format_exc()
                log_(log_file_name_entity_matching_general,formatted_lines)