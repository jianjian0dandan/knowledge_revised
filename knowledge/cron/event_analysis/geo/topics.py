# -*- coding: utf-8 -*-
'''定制话题表管理
'''


import time
from config import db
from model import Topics


EXPIRE_TS = 1577808000 # 2020-01-01 1.1


def _all_topics(iscustom=None):
    # 返回所有的话题
    if not iscustom:
	topics = Topics.query.all()
    else:
    	topics = Topics.query.filter_by(iscustom=iscustom).all()

	return topics


def _drop_topic(topic, user='admin', iscustom=True, expire_date=int(time.time())):
    # 不物理删除话题，设置话题过期时间expire date为当前时间，并将iscustom设置成False
    if iscustom:
        item = Topics(user, topic, False, expire_date)
        exist_item = Topics.query.filter_by(topic=topic).first()
        
        if exist_item and exist_item.iscustom:
            db.session.delete(exist_item)
            db.session.add(item)
            db.session.commit()
            return 'success', item
        else:
            return 'failed', item


def _add_topic(topic, user='admin', iscustom=True, expire_date=EXPIRE_TS):
	if iscustom:
	    item = Topics(user, topic, iscustom, expire_date)
	    exist_item = Topics.query.filter_by(topic=topic, iscustom=True).first()
	    expire_item = Topics.query.filter_by(topic=topic, iscustom=False).first()
	    
	    if not expire_item and not exist_item:
	        db.session.add(item)
	        db.session.commit()

	        return 'success', item

	    elif exist_item:

	    	return 'exist', exist_item

	    else:
	    	db.session.delete(expire_item)
	    	db.session.add(item)
	        db.session.commit()

	    	return 'success', item


def _topic_not_custom_and_expire(now_ts):
	topics = db.session.query(Topics).filter(Topics.iscustom==False, \
		                                       Topics.expire_date<=now_ts).all()
	return topics


def _search_topic(topic, iscustom=True):
	exist_item = Topics.query.filter_by(topic=topic, iscustom=True).all()
	if exist_item:
		return exist_item
	else:
		return None