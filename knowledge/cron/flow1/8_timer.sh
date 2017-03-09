#!/bin/sh
tmux kill-session -t work
python flushdb.py

tmux new-session -s flow1 -d
tmux new-window -n first -t flow1
tmux new-window -n vent -t flow1
tmux new-window -n work1 -t flow1
tmux new-window -n work2 -t flow1
tmux new-window -n work3 -t flow1
tmux new-window -n work4 -t flow1
tmux send-keys -t flow1:vent 'python zmq_vent_weibo.py' C-m
tmux send-keys -t flow1:work1 'python zmq_work_weibo.py' C-m
tmux send-keys -t flow1:work2 'python zmq_work_weibo.py' C-m
tmux send-keys -t flow1:work3 'python zmq_work_weibo.py' C-m
tmux send-keys -t flow1:work4 'python zmq_work_weibo.py' C-m

python restart_zmq_vent.py


