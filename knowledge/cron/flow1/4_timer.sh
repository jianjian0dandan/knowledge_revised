#!/bin/sh
#cd /home/ubuntu8/yuankun/new_version/user_portrait/user_portrait/cron/flow1
tmux kill-session -t flow1

tmux new-session -s work -d
tmux new-window -n first -t work
tmux new-window -n redis -t work
tmux new-window -n es1 -t work
tmux new-window -n es2 -t work
tmux new-window -n es3 -t work
tmux new-window -n es4 -t work
tmux send-keys -t work:redis 'python send_uid.py' C-m
tmux send-keys -t work:es1 'python redis_to_es.py' C-m
tmux send-keys -t work:es2 'python redis_to_es.py' C-m
tmux send-keys -t work:es3 'python redis_to_es.py' C-m
tmux send-keys -t work:es4 'python redis_to_es.py' C-m

#ps -ef |grep zmq_work_weibo.py| grep -v grep | cut -c 9-15|xargs kill -s 9
#ps -ef |grep zmq_vent_weibo.py| grep -v grep | cut -c 9-15|xargs kill -s 9

