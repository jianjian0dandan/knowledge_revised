import sys
import json
import pinyin
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_prediction as es
from global_config import index_event_time_count,type_event_time_count,\
							index_event_time_kcount,type_event_time_kcount,\
							index_event_time_weibo,type_event_time_weibo


def mappings_event_time_count():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_time_count:{
				'properties':{
					'en_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'end_ts':{
						'type':'long'
					},
					'range':{
						'type':'long'
					},
					'mtype':{
						'type':'string',
						'index':'not_analyzed'
					},
					'count':{
						'type':'long'
					}
				}
			}

		}

	}

	if not es.indices.exists(index=index_event_time_count):
		es.indices.create(index=type_event_time_count, body=index_info, ignore=400)


def mappings_event_time_kcount():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_time_kcount:{
				'properties':{
					'en_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'end_ts':{
						'type':'long'
					},
					'range':{
						'type':'long'
					},
					'mtype':{
						'type':'string',
						'index':'not_analyzed'
					},
					'limit':{
						'type':'long'
					},
					'kcount':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}

		}

	}

	if not es.indices.exists(index=index_event_time_kcount):
		es.indices.create(index=index_event_time_kcount, body=index_info, ignore=400)



def mappings_event_time_weibo():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_time_weibo:{
				'properties':{
					'en_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'end_ts':{
						'type':'long'
					},
					'range':{
						'type':'long'
					},
					'mtype':{
						'type':'string',
						'index':'not_analyzed'
					},
					'limit':{
						'type':'long'
					},
					'weibo':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}

		}

	}

	if not es.indices.exists(index=index_event_time_weibo):

		es.indices.create(index=index_event_time_weibo, body=index_info, ignore=400)
