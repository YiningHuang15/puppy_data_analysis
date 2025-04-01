#!/bin/bash

echo "=== Running Kirby Tracker Load at $(date) ===" >> /Users/yi-ninghuang/Documents/Python_Project/log/run_kirby_tracker_load.log

/Users/yi-ninghuang/opt/anaconda3/bin/python3 /Users/yi-ninghuang/Documents/Python_Project/bin/kirby_tracker_loader.py >> /Users/yi-ninghuang/Documents/Python_Project/log/run_kirby_tracker_load.log 2>&1

if [ $? -eq 0 ]; then
    echo "Kirby Tracker Load Successful" >> /Users/yi-ninghuang/Documents/Python_Project/log/run_kirby_tracker_load.log
else
    echo "Kirby Tracker Load Failed" >> /Users/yi-ninghuang/Documents/Python_Project/log/run_kirby_tracker_load.log
fi
