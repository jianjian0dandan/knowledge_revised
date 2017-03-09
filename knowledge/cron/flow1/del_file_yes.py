# -*- coding = utf-8 -*-

import os

path = "../weibo_1/weibo"
file_list = os.listdir(path)
for each in file_list:
    filename = each.split('.')[0]
    if filename.split('_')[-1] == 'yes':
        os.remove(path+'/'+each)
