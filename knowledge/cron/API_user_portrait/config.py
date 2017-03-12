# -*- coding: UTF-8 -*-

#topic en2ch dict
topic_en2ch_dict = {'art':u'文体类_娱乐','computer':u'科技类','economic':u'经济类', \
           'education':u'教育类','environment':u'民生类_环保', 'medicine':u'民生类_健康',\
           'military':u'军事类','politics':u'政治类_外交','sports':u'文体类_体育',\
           'traffic':u'民生类_交通','life':u'其他类','anti-corruption':u'政治类_反腐',\
           'employment':u'民生类_就业','fear-of-violence':u'政治类_暴恐',\
           'house':u'民生类_住房','law':u'民生类_法律','peace':u'政治类_地区和平',\
           'religion':u'政治类_宗教','social-security':u'民生类_社会保障'}

#activeness weight dict used by evaluate_index.py
activeness_weight_dict = {'activity_time':0.3, 'activity_geo':0.2, 'statusnum':0.5}
#importance weight dict
importance_weight_dict = {'fansnum':0.2, 'domain':0.5, 'topic':0.3}
#topic weight dict
'''
topic_weight_dict = {'政治':0.3, '军事':0.15, '社会':0.15, '环境':0.05, \
                      '医药':0.05, '经济':0.05, '交通':0.05, '教育':0.05, \
                      '计算机':0.05, '艺术':0.05, '体育':0.05}
'''

topic_weight_dict = {'文体类_娱乐':0.2,'科技类':0.3,'经济类':0.5,'教育类':0.5, \
                     '民生类_环保':0.3,'民生类_健康':0.3, '军事类':0.8 ,'政治类_外交':0.8,\
                     '文体类_体育':0.2,'民生类_交通':0.3,'其他类':0.2,\
                     '政治类_反腐':0.8,'民生类_就业':0.5,'政治类_暴恐':1 ,\
                     '民生类_住房':0.4,'民生类_法律':0.7,\
                     '政治类_地区和平':0.9, '政治类_宗教':0.8,'民生类_社会保障':0.6}


#domain en2ch dict
domain_en2ch_dict = {'university':u'高校', 'homeadmin':u'境内机构', 'abroadadmin':u'境外机构', \
                     'homemedia':u'媒体', 'abroadmedia':u'境外媒体', 'folkorg':u'民间组织',\
                     'lawyer':u'法律机构及人士', 'politician':u'政府机构及人士', 'mediaworker':u'媒体人士',\
                     'activer':u'活跃人士', 'grassroot':u'草根', 'other':u'其他', 'business':u'商业人士'}

#domain weight dict
domain_weight_dict = {'高校':0.8, '境内机构':0.6, '境外机构':1, '媒体':1, \
                      '境外媒体':1, '民间组织':0.8,'法律机构及人士':1, '政府机构及人士':0.8,\
                      '媒体人士':0.8, '活跃人士':0.6, '草根':0.6, '其他':0.5, '商业人士':0.6}