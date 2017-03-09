import sys
import json
import pinyin
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_prediction as es
from global_config import index_event_geo_city_repost,type_event_geo_city_repost,\
						 index_event_geo_province_weibos,type_event_geo_province_weibos,\
						 index_event_geo_city_topic_count,type_event_geo_city_topic_count
							

def mappings_event_geo_city_repost():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_geo_city_repost:{
				'properties':{
					'en_name':{
						'type':'string',
						'index':'not_analyzed'
					},
					'original':{             # 原创值为1，转发值为0
						'type':'long'
					},
					'mid':{
						'type':'string',
						'index':'not_analyzed'
					}
					'timestamp':{
						'type':'long'
					},
					'origin_location':{      # 原始微博发布地点
						'type':'string',
						'index':'not_analyzed'
					},
					'repost_location':{      # 转发微博发布地点
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}

		}

	}

	if not es.indices.exists(index=index_event_geo_city_repost):

        es.indices.create(index=index_event_geo_city_repost, body=index_info, ignore=400)


def mappings_event_geo_province_weibos():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_geo_province_weibos:{
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
					'limit':{
						'type':'long'
					},
					'province':{
						'type':'string',
						'index':'not_analyzed'
					},
					'city':{
						'type':'string',
						'index':'not_analyzed'
					},
					'weibo':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}

		}

	}

	if not es.indices.exists(index=index_event_geo_province_weibos):

        es.indices.create(index=index_event_geo_province_weibos, body=index_info, ignore=400)



def mappings_event_geo_city_topic_count():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_geo_city_topic_count:{
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
					'mtype':{                     #message_type:原创-1、转发-2、评论-3
						'type':'string',
						'index':'not_analyzed'
					},
					'ccount':{                    #city_count:{city:count}
						'type':'string',
						'index':'not_analyzed'
					},
					'first_item':{
						'type':'string',           # 原创 初始微博 其他类型为空
						'index':'not_analyzed'
					}
				}
			}

		}

	}

	if not es.indices.exists(index=index_event_geo_city_topic_count):

        es.indices.create(index=index_event_geo_city_topic_count, body=index_info, ignore=400)
