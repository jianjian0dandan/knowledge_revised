# -*- coding: UTF-8 -*-
'''
use to compute @ constructure
'''
import re
import json
import time
import redis
from test_save_attribute import save_at

# extract uname from text
def extract_uname(text):
    at_uname_list = []
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    # extract text from long retweet weibo
    text = text.split('//@')[0]
    RE = re.compile(u'@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+) ', re.UNICODE)
    repost_chains = RE.findall(text)

    return repost_chains

#extract @ uname to uid and +1
def accumulate_at(item2dict):
    weibo = item2dict
    text = weibo['text']
    uid = weibo['user']
    timestamp = weibo['timestamp']
    at_uname_list = extract_uname(text)
    try:
        at_uname = at_uname_list[0]
        save_at(uid, at_uname, timestamp)
    except:
        pass
    
  
