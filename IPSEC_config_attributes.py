#!/usr/bin/env python

Import argparse
import paramiko
import time
import re

# Parse Args (Results in the script being executed like "python scriptname.py -i 192.168.1.1")
parser = argparse.ArgumentParser() #Set up Parser
host_help = "Enter the host ip address" #Help text shown on CL when -h
parser.add_argument("-i", "--ipaddress", help=host_help, dest='host_ip', type=int) #Actual parser rule see https://docs.python.org/2/howto/argparse.html
input_args = parser.parse_args() #Actually parse the input to a varable you can reference
host = input_args.host_ip

# Variables
host = MYDEVICEHOSTNAME = '1.1.1.1'

# Create instance of SSHClient object
ssh = paramiko.SSHClient()

# Automatically add untrusted hosts
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Automatically add untrusted hosts
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# initiate SSH connection
ssh.connect('MYDEVICEHOSTNAME', port=22, username='username', password='password', look_for_keys=False, allow_agent=False)
print "SSH Connection established with %s" % host

# Use invoke_shell to establish an 'interactive session'
ssh_conn = ssh.invoke_shell()
print "Interactive SSH session established"

print "Give the name of the 3PPartner\n"
partner = raw_input('>')

# Commands prompted
ssh_conn.send('\n')
ssh_conn.send('enable\n')
time.sleep(.5)
ssh_conn.send('myenablepassword4\n')
time.sleep(.5)
ssh_conn.send("terminal pager 0\n")
time.sleep(.5)
ssh_conn.send('show running-config crypto map | i ' + str(partner) + '\n')
time.sleep(.5)
output_0 = ssh_conn.recv(65535)
print output_0

print "Which crypto map you want see?\n"
crypto = raw_input('>')
ssh_conn.send('show running-config crypto map | i ' + str(crypto) + '\n')
time.sleep(.5)
output_1 = ssh_conn.recv(65535)
print output_1
time.sleep(.5)

crypto_acl = re.findall("(?<=address\s)[-\w+]*", output_1)
for match in crypto_acl:
    ssh_conn.send('show running-config access-list ' + match + '\n')
    time.sleep(.5)
    output_3 = ssh_conn.recv(65535)
    print output_3

acl_entry = re.findall("(?<=object-group\s)[-\w+]*", output_3)
for match in acl_entry:
    ssh_conn.send('show running-config object-group id ' + match + '\n')
    time.sleep(.5)
    ssh_conn.send('show running-config access-list transit-in | i ' + match + '\n')
    time.sleep(.5)
    ssh_conn.send('show running-config access-list outside-in | i ' + match + '\n')
    time.sleep(.5)
    ssh_conn.send('show running-config nat | i ' + match + '\n')
    time.sleep(.5)
    output_4 = ssh_conn.recv(65535)
    print output_4

# Close session
ssh.close()
print 'Logged out of device %s' %host

#f20171029
