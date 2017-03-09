#!/bin/sh
tmux new-window -n stop -t flow1
tmux send-keys -t flow1:stop 'python stop_zmq_vent.py' C-m

