import sys
import json
import pinyin
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_prediction as es
from global_config import index_event_sentiment_count,type_event_sentiment_count,\
							index_event_sentiment_geo,type_event_sentiment_geo,\
							index_event_sentiment_weibo,type_event_sentiment_weibo


def mappings_event_sentiment_count():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_sentiment_count:{
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
					'sentiment':{
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

	if not es.indices.exists(index=index_event_sentiment_count):

        es.indices.create(index=index_event_sentiment_count, body=index_info, ignore=400)



def mappings_event_sentiment_weibo():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_sentiment_weibo:{
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
					'sentiment':{
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

	if not es.indices.exists(index=index_event_sentiment_weibo):

        es.indices.create(index=index_event_sentiment_weibo, body=index_info, ignore=400)


def mappings_event_sentiment_geo():

	index_info = {
		'settings':{
			'numbers_of_replicas':0,
			'numbers_of_shards':5
		},
		'mappings':{
			type_event_sentiment_geo:{
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
					'sentiment':{
						'type':'string',
						'index':'not_analyzed'
					},
					'geo_count':{
						'type':'string',
						'index':'not_analyzed'
					}
				}
			}

		}

	}

	if not es.indices.exists(index=index_event_sentiment_geo):

        es.indices.create(index=index_event_sentiment_geo, body=index_info, ignore=400)

