# -*- coding: UTF-8 -*-
import time
import csv

word_dict = {'126':[], '127':[], '128':[], '129':[]}

def main():
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/sc_liwc.dic', 'rb')
    count = 0
    for line in f:
        count += 1
        if count>=74:
            line1 = line.split('\n')[0]
            line2 = line1.split('\r')[0]
            word_list = line2.split('\t')
            #print 'line:', line2
            #print 'word_list:', word_list
            n = len(word_list)
            word = word_list[0].split('*')[0].decode('utf-8')
            for i in  range(1, n):
                num = word_list[i]
                if str(num) in word_dict:
                    word_dict[str(num)].append(word)
    #print 'word_dict:', word_dict
    f.close()
    csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow2/extract_word.csv', 'wb')
    writer = csv.writer(csvfile)
    for num in word_dict:
        word_list = word_dict[num]
        for word in word_list:
            writer.writerow([num, word.encode('utf-8')])
    csvfile.close()

if __name__=='__main__':
    main()
