# -*- coding: UTF-8 -*-
import os
import time
import scws
import csv
import sys
import json
from sys import argv
from get_similarity  import *
from config import *
sys.path.append('../../')
from global_config import *

def compute_sim_by_id(node_type,node_id):
	es_sim.update(index=sim_name,doc_type=sim_type,id=node_id,body={'doc':{'compute_status':-1}})
	print node_type,node_id
	print 'start:',time.time()
	if node_type == people_node or node_type == org_node:
		node_dict = get_people_att_by_keys([node_id])
		id_list = people_similarity(node_dict.values()[0])
	elif node_type == event_node:
		event_dict = get_event_att_by_keys([node_id])
		id_list = event_similarity(event_dict.values()[0])
	elif node_type == group_node:
		id_list = crowd_similarity(node_id)
	else:
		id_list = topic_similarity(node_id)
	print id_list
	print 'end:',time.time()
	print es_sim.update(index=sim_name,doc_type=sim_type,id=node_id,body={'doc':{'compute_status':1,'related_id':'&'.join(id_list)}})


if __name__ == '__main__':
	node_type = argv[1]
	node_id = argv[2]
	compute_sim_by_id(node_type,node_id)
