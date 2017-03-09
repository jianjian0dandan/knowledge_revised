# -*- coding:utf-8 -*-

import subprocess
import sys
import os
import time

def check(p_name):
    cmd = 'ps -ef|grep %s|grep -v "grep"' % p_name
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if p.wait() == 0:
        val = p.stdout.read()
        #print val
        if p_name in val:
            print "%s %s running" % (time.ctime(),p_name)
    else:
        os.system("python ./%s &" % p_name)
        print "%s %s restart" % (time.ctime(), p_name)


if __name__ == '__main__':
    # 查询zmq_vent_weibo.py是否在执行
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'redis_to_es.py')
    ts = str(int(time.time()))
    print_log = "&".join([file_path, "start", ts])
    print print_log #打印开始信息

    d_name = 'zmq_vent_weibo.py'
    #check(item)

    ts = str(int(time.time()))
    print_log = "&".join([file_path, "end", ts])
    print print_log

