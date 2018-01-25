import os
import sys
import socket
import time

from collections import OrderedDict


#
# pip install collections-extended

def interact(sock):
     command = ''
     switch  = 0
     
     while(command != 'exit'):
         command=raw_input('')
         sock.send(command + '\n')
         time.sleep(.5)
         if switch == 0:
             buffer = sock.recv(0x10000)
             for line in OrderedDict.fromkeys(buffer.splitlines()):
                sys.stdout.write("\n"+line)

             switch += 1
             
         else:  
            sys.stdout.write(sock.recv(0x10000))
     return

def run(HOST,PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, int(PORT)))
    s.listen(1)

    sock , addr = s.accept()
    interact(sock)
