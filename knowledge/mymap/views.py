# -*-coding:utf-8-*-
from flask import Blueprint, request, make_response, render_template
from  landing_module import select_user, update_itme, insert_item, delete_item, login_administrator
from user_interface import login, select_topic, delete_topic, insert_topic, select_group, delete_group, insert_group, \
    select_people, insert_people, delete_people, insert_event, delete_event, select_event, insert_event_history, \
    select_people_history,insert_people_history,select_event_history
import json
import datetime

# from knowledge.global_utils import event_name_search

mod = Blueprint('mymap', __name__, url_prefix='/mymap')


#################################################################################
# 管理员用户操作

# 查询有多少个用户
@mod.route('/mysql_user_select/')
def select_users():
    result = select_user()
    return json.dumps(result)


# 修改一个用户的密码
@mod.route('/mysql_user_update/')
def update_users():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    if user == '' or password == '':
        print "user or password is null"
        return '0'
    else:
        result = update_itme(user, password)
        return str(result)


# 添加一个用户
@mod.route('/mysql_user_insert/')
def insert_users():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    if user == '' or password == '':
        print "user or password is null"
        return '0'
    else:
        result = insert_item(user, password)
        return str(result)


# 删除一个用户
@mod.route('/mysql_user_delete/')
def delete_users():
    user = request.args.get('user', '')
    if user == '':
        print "user  is null"
        return '0'
    else:
        result = delete_item(user)
        return str(result)


# 管理员用户进行登录
@mod.route('/mysql_user_admin_login/')
def login_admin():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    if user == '' or password == '':
        print "user or password is null"
        return '0'
    else:
        result = login_administrator(user, password)
        return str(result)


######################################################################


# 用户登录界面
@mod.route('/mysql_user_login/')
def login_user():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    if user == '' or password == '':
        print "user or password is null"
        return '0'
    else:
        result = login(user, password)
        if result != 0:
            response = make_response("1")
            response.set_cookie("user", user)
            print "user+++++++"+user   
            ##############################################需要进行修改
            return response
        else:
            return "0"


# 查询当前用户所有的专题
@mod.route('/select_topic/')
def select_topics():
    user = request.cookies.get("user")
    if user != None:
        result = select_topic(user)
        list = []
        for item in result:
            sdb = (item[1], item[2], item[3], item[4], str(item[5]), str(item[6]))
            list.append(sdb)
        return json.dumps(list)
    else:
        return ""


# 删除该用户的专题
@mod.route('/delete_topic/')
def delete_topics():
    user = request.cookies.get("user")
    topicName = request.args.get('topicname', '')
    if user != None and topicName != '':
        result = delete_topic(user, topicName)
        return str(result)
    else:
        return "0"


# 添加一个新的专题
@mod.route('/insert_topic/')
def insert_topics():
    user = request.cookies.get("user")
    list = request.args.get('list', '')
    if user != None and list != '':
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list = (user, list(0), list(1), list(2), dt, dt)
        result = insert_topic(list)
        return str(result)
    else:
        return "0"


# 差一个修改的界面——如何修改？
#########################################################################
# 我的群体


# 查询当前用户所有的群体
@mod.route('/select_group/')
def select_groups():
    user = request.cookies.get("user")
    if user != None:
        result = select_group(user)
        list = []
        for item in result:
            sdb = (item[1], item[2], item[3], item[4], str(item[5]), str(item[6]))
            list.append(sdb)
        return json.dumps(list)
    else:
        return ""


# 删除该用户的专题
@mod.route('/delete_group/')
def delete_groups():
    user = request.cookies.get("user")
    groupName = request.args.get('groupname', '')
    if user != None and groupName != '':
        result = delete_group(user, groupName)
        return str(result)
    else:
        return "0"


# 添加一个新的专题
@mod.route('/insert_group/')
def insert_groups():
    user = request.cookies.get("user")
    list = request.args.get('list', '')
    if user != None and list != '':
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list = (user, list(0), list(1), list(2), dt, dt)
        result = insert_group(list)
        return str(result)
    else:
        return "0"


####################################################################
# 我关注的人

# 查询当前用户所有关注的人
@mod.route('/select_people/')
def select_peoples():
    user = request.cookies.get("user")
    if user != None:
        result = select_people(user)
        list = []
        for item in result:
            sdb = (item[2], item[3], str(item[4]))
            list.append(sdb)
        return json.dumps(list)
    else:
        return ""


# 删除该用户的关注
@mod.route('/delete_people/')
def delete_peoples():
    user = request.cookies.get("user")
    peopleID = request.args.get('peopleid', '')
    if user != None and peopleID != '':
        result = delete_people(user, peopleID)
        return str(result)
    else:
        return "0"


# 添加一个新的关注的人
@mod.route('/insert_people/')
def insert_peoples():
    user = request.cookies.get("user")
    list = request.args.get('list', '')
    if user != None and list != '':
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list = (user, list(0), list(1), dt)
        result = insert_people(list)
        return str(result)
    else:
        return "0"


##############################################################
# 我说关注的事件


# 查询当前用户所有关注的事件
@mod.route('/select_event/')
def select_events():
    user = request.cookies.get("user")
    print user
    if user != None:
        result = select_event(user)
        list = []
        for item in result:
            sdb = (item[2], item[3], str(item[4]))
            list.append(sdb)
        return json.dumps(list)
    else:
        return ""


# 删除该用户的关注事件
@mod.route('/delete_event/')
def delete_events():
    user = request.cookies.get("user")
    eventID = request.args.get('eventid', '')
    if user != None and eventID != '':
        result = delete_event(user, eventID)
        return str(result)
    else:
        return "0"


# 添加一个新的关注的事件
@mod.route('/insert_event/')
def insert_events():
    user = request.cookies.get("user")
    list = request.args.get('list', '')
    if user != None and list != '':
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list = (user, list(0), list(1), dt)
        result = insert_event(list)
        return str(result)
    else:
        return "0"


###########################################################################
# 人物修改记录


# 添加一条修改人物记录
@mod.route('/insert_people_history/')
def insert_people_historys():
    user = request.cookies.get("user")
    list = request.args.get('list', '')
    if user != None and list != '':
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list = (user, list(0), list(1), dt)
        result = insert_people_history(list)
        return str(result)
    else:
        return "0"


# 查询修改人物记录
@mod.route('/select_people_history/')
def select_people_historys():
    result = select_people_history()
    list = []
    for item in result:
        sdb = (item[1], item[2], item[3], str(item[4]))
        list.append(sdb)
    return json.dumps(list)


###############################################################################
#事件修改记录


#添加人物的修改记录
@mod.route('/insert_event_history/')
def insert_event_historys():
    user = request.cookies.get("user")
    list = request.args.get('list', '')
    if user != None and list != '':
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list = (user, list(0), list(1), dt)
        result = insert_event_history(list)
        return str(result)
    else:
        return "0"


# 查询修改事件记录
@mod.route('/select_event_history/')
def select_event_historys():
    result = select_event_history()
    list = []
    for item in result:
        sdb = (item[1], item[2], item[3], str(item[4]))
        list.append(sdb)
    return json.dumps(list)

@mod.route('/get_session/')
def get_sessions():
    user = request.cookies.get("user")
    print user
    return "1"



@mod.route('/set_session/')
def set_sessions():
    response = make_response("username_login")
    response.set_cookie("user", "zhaishujie")
    return "1"



