# coding=utf-8
import MySQLdb
from knowledge.global_utils import mysql_charset,mysql_db,mysql_host,mysql_passwd,mysql_port,mysql_user
import hashlib


def getconn():
    conn = MySQLdb.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        passwd=mysql_passwd,
        db=mysql_db,
        charset=mysql_charset
    )
    return conn


def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def closeAll(conn, cur):
    cur.close()
    conn.commit()
    conn.close()



