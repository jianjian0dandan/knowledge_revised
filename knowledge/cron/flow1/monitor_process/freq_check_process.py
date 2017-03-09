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
        if p_name in val:
            print "%s %s running" % (time.ctime(), p_name)
    else:
        os.system("python ./%s &" % p_name)
        print "%s %s restart" % (time.ctime(), p_name)


if __name__ == '__main__':

    d_name = ['redis_to_es.py','zmq_vent_weibo.py', 'zmq_work_weibo.py']
    for item in d_name:
        check(item)

