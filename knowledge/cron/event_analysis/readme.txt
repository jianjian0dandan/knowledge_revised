#安装 libsvm-3.1.7
#225所在文件夹 /home/ubuntu2/jiangln/info_consume/user_portrait/user_portrait/cron/libsvm-3.17
#安装community 用pip install community 和 pip install python-louvain==0.2


network/cron_topic_identify.py中也有pagerank()




时间：
输入：
输出：

地域：
输入：
输出：

网络：

输入：
输出：
生成的网络（gexf）存在了es中
trend_maker和trend_pusher是放在了mysql中。



event中五个维度的utils.py都是从mysql中取的数据。

时间：

get_time_count（）  mysql  -----  PropagateCount

get_weibo_by_time（）es——weibo_es

地域：

province_weibo_count（）  mysql  ----- CityTopicCount

get_weibo_content()       mysql  ----- ProvinceWeibos

网络：

get_gexf（） -----》 read_long_gexf（）  es ---- weibo_es

gexf_process() 处理的为get_gexf（） 取出的数据，不涉及到sql和es

get_trend_maker（）     mysql  ----  TrendMaker

get_trend_pusher()       mysql  -----  TrendPusher

get_maker_weibos_byts()  mysql  ----- TrendMaker

get_pusher_weibos_byts()  mysql  ----  TrendPusher

get_maker_weibos_byhot()  mysql  ---- TrendMaker

get_pusher_weibos_byhot()  mysql ---  TrendPusher


情感：

get_sen_time_count（）  mysql ---- SentimentCount

get_sen_province_count()  mysql ---- SentimentGeo

get_weibo_content()       mysql ----- SentimentWeibos


语义：

get_during_keywords（）   es  ----  weibo_es

get_topics_river()  -----> cul_key_weibo_time_count()    二者都是   es  ----- weibo_es   

get_symbol_weibo（）     es   ----  weibo_es

get_subopinion()         es   ----  weibo_es

 




