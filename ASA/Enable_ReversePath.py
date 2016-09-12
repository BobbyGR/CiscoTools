import paramiko
import time
import os
import sys
import mmap
import getpass
from sys import argv
import re


def disable_paging(remote_conn):
    remote_conn.send("terminal length 0\n")
    time.sleep(1)
    output = remote_conn.recv(1000)
    return output

if __name__ == '__main__':
    Interface = os.path.dirname(os.path.realpath(__file__)) + "/FW_Interfaces.txt"
    if not os.path.exists(Interface):
        f = file(Interface, "w")
    target = open(Interface, 'w')
    target.truncate()
    target.close()
    STUFF,IP_ADDR = argv
    username = raw_input("Enter Username: ")
    password = getpass.getpass("Enter Username Password: ")
    EnablePassword = getpass.getpass("Enter Enable Password: ")
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    IP_ADDR = str(IP_ADDR)
    try:
	print IP_ADDR
        remote_conn_pre.connect(IP_ADDR, username=username, password=password, allow_agent=False, timeout=5)
        print "SSH connection established to " + IP_ADDR
        remote_conn = remote_conn_pre.invoke_shell()
        output = remote_conn.recv(1000)
    except ValueError:
        print "Failed connection to " + IP_ADDR
    try:
	remote_conn.send("en\n")
	time.sleep(1)
	remote_conn.send(EnablePassword + "\n")
	time.sleep(1)
        remote_conn.send("conf t\n")
        time.sleep(1)
        remote_conn.send("ip verify reverse-path interface ?\n")
        time.sleep(1)
        output = remote_conn.recv(5000)
    except ValueError:
        print "Failed talking to " + IP_ADDR
    try:
        with open(Interface, "a") as myfile:
            myfile.write(output)
    except ValueError:
	    print "YOLO"
    f = open(Interface, 'r')
    lines = f.readlines()
    for line in lines:
	    if re.match("(.*)Name (.*)", line):
		    re1='((?:[a-z][a-z0-9_]*))'
		    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
		    m = rg.search(line)
		    if m:
		       INT_NAME=m.group(1)
		       print (INT_NAME)
		       try:
			 remote_conn_pre.connect(IP_ADDR, username=username, password=password, allow_agent=False, timeout=5)
			 remote_conn = remote_conn_pre.invoke_shell()
			 remote_conn.send("en\n")
			 time.sleep(1)
			 remote_conn.send(EnablePassword + "\n")
			 time.sleep(1)
			 remote_conn.send("conf t\n")
			 time.sleep(1)
			 remote_conn.send("ip verify reverse-path interface " +  INT_NAME + "\n")
			 time.sleep(2)
			 remote_conn.close()
		       except ValueError:
			 print "Something bad happened..."
