#!/bin/sh

while true; do
  nohup python agent.py >> /dev/null # Modify this to catch the quit error 
done &