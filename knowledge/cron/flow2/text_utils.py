# -*- coding: UTF-8 -*-
import sys
import csv

f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/ZZ_uid07.csv', 'wb')
writer = csv.writer(f)

# deal with sensitive word
def sensitive_word():
    f1 = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/zz.txt', 'rb')
    ZZ_WORD = []
    for line in f1:
        line_list = line.split('=')
        word = line_list[0]
        print 'word:', word, type(word.decode('utf-8'))
        ZZ_WORD.append(word.decode('utf-8'))
    print 'len(ZZ_WORD):', len(ZZ_WORD)
    f1.close()
    return ZZ_WORD
        
ZZ_WORD = sensitive_word()
        
        
sensitive_user = dict()

# compute text attribute
def accumulate_text(user, text):
    for word in ZZ_WORD:
        if word in text:
            try:
                sensitive_user[user] += 1
            except:
                sensitive_user[user] = 1
            writer.writerow([str(user), word.encode('utf-8'), text.encode('utf-8')])
            #print 'user, text, word:',type(user), type(text), type(word)

def write_sensitive_user():
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/sensitive_user_rank07.csv', 'wb')
    f_writer = csv.writer(f)
    sort_user = sorted(sensitive_user.items(), key=lambda x:x[1], reverse=True)
    for item in sort_user:
        user = item[0]
        rank = item[1]
        f_writer.writerow([user, rank])
    f.close()


if __name__=='__main__':
    sensitive_word()
