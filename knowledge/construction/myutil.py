# -*-coding:utf-8-*-
def get_type_key(item):
    if item == 1:
        return "uid"
    elif item == 2:
        return "event_id"
    elif item == 0:
        return 'org_id'
    else:
        return 'uid'
    
