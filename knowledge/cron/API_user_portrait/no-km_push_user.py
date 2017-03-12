# -*-coding:utf-8-*-

import sys
reload(sys)
sys.path.append("../../")
from global_utils import r_user


#r.lpush("uid_list", "3229125510")
print r.lpop("uid_list")


