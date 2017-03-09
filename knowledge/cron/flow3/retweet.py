# -*- coding: UTF-8 -*-
'''
use to compute retweet relationship
'''
import re
import json
import time
import redis
from test_search_user_profile import search_uname2uid
from test_save_attribute import save_ruid

#get direct superior uid
def get_ds_uid(text):
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
    repost_chains = RE.findall(text)

    if repost_chains!=[]:
        r_uname = repost_chains[0]
    else:
        return None
    r_uid = search_uname2uid(r_uname)
    
    return r_uid
    
# main function to accumulate retweet relationship
def accumulate_retweet(item2dict):
    weibo = item2dict
    uid = weibo['user']
    '''
    text = weibo['text']
    direct_superior_uid = get_ds_uid(text)
    if not direct_superior_uid:
        r_uid = weibo['retweeted_uid']
    else:
        r_uid = direct_superior_uid
    '''
    r_uid = weibo['retweeted_uid']
    timestamp = weibo['timestamp']
    save_ruid(uid, r_uid, timestamp)
