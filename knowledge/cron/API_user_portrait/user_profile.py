# -*- coding: UTF-8 -*-
'''
acquire the profile information from user_profile
input: uid_list
output: {uid:{attr:value}}
'''
import sys
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_user_profile as es
from global_utils import profile_index_name as index_name
from global_utils import profile_index_type as index_type
fields_dict = {'uname':"nick_name", 'gender':"sex", 'location':"user_location", \
               'verified':"isreal", 'verified_type': 'verified_type', \
               'photo_url':"photo_url", 'description': 'description', \
               'born_data':'born_data', 'real_name':'real_name'}


def get_profile_information(uid_list):
    result_dict = dict()
    search_result = es.mget(index=index_name, doc_type=index_type, body={'ids':uid_list}, _source=True)['docs']
    iter_count = 0
    for item in search_result:
        user_dict = {}
        for field in fields_dict:
            try:
                user_dict[field] = item['_source'][field]
            except:
                user_dict[field] = ''
        result_dict[item['_id']] = user_dict
        iter_count += 1
    return result_dict