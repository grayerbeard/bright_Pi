#!/bin/bash
cd /home/pi/leds
echo looking to kill any old tmux leds session
tmux kill-session -t leds
echo now new tmux leds session 
tmux new-session -d -s leds 'python3 lamps.py'
