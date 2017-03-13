# -*-coding:utf-8-*-

def get_type_key(item):
    if item == 1:
        return "uid"
    elif item == 2:
        return "event"
    elif item == 0:
        return 'org'
    else:
        return 'uid'
