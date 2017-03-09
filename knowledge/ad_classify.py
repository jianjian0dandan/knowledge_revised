# -*- coding: utf-8 -*-

import os
import sys
import random

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libsvm-3.17/python/')

sys.path.append(AB_PATH)

from sta_ad import start

def ad_classifier(rlist):
    flag =  str(random.randint(1, 100))
    data = start(rlist, flag)
    
    return len(data), data