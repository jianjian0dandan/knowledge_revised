# coding=utf-8
from mysql_util import getconn, closeAll, md5
from flask import Flask,make_response,request


"""
这个文件的代码主要是针对管理员用户进行的增加删除修改操作的。
其中包括简单的防sql注入以及加密会让系统更加安全。
在数据库中我们不在已经明文进行数据的存储。
"""


# 查询用户
def select_user():
    conn = getconn()
    cur = conn.cursor()
    sql = "select * from user"
    count = cur.execute(sql)
    result = cur.fetchmany(count)
    return result


# 添加用户
def insert_item(username, password):
    password = md5(password)
    conn = getconn()
    cur = conn.cursor()
    sql = "insert into user (name,password) values (%s,%s)"
    result = cur.execute(sql, (username, password))
    closeAll(conn, cur)
    return result


# 修改密码
def update_itme(username, password):
    conn = getconn()
    cur = conn.cursor()
    password = md5(password)
    sql = "update user set password='%s' where name = '%s'" % (password, username)
    print sql
    result = cur.execute(sql)
    closeAll(conn, cur)
    return result


# 删除一个用户
def delete_item(username):
    conn = getconn()
    cur = conn.cursor()
    sql = "delete from user where name='%s'" % (username)
    result = cur.execute(sql)
    closeAll(conn, cur)
    return result


# 登录超级管理员帐号
def login_administrator(username, password):
    if username == 'admin' and password == "admin":

        return 1
    else:
        return 0


if __name__ == '__main__':
    response = make_response("hellow")
    response.set_cookie("Name","zhaishujie")
    request.cookies.get("Name")