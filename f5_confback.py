#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

from getpass import getpass
import json
import netmiko
from netmiko.f5.f5_ltm_ssh import F5LtmSSH
#from netmiko import ConnectHandler
#from netmiko.cisco import CiscoIosBase (device type: "cisco_ios", "cisco_xe")
#from netmiko.cisco import CiscoIosBase (device type: "cisco_xe")
import sys
import signal
import os
import commands

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_credentials():
    """Prompt for and return a username and password."""
    username = get_input('Username(Please input your adm credentials): ')
    password = getpass()
    return username, password

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = get_credentials()


os.system('find *f5.json')
os.system('echo')
os.system('echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"')
devicegroup = raw_input("Please select which device-group you want to apply to: \n")


with open(devicegroup) as dev_file:
    devices = json.load(dev_file)


for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print('~' * 80)
        print('Connecting to device:', device['ip'])
        connection = netmiko.ConnectHandler(**device)
        filename = device['ip'] + '.cfg'
        with open(filename, 'w') as out_file:
            print(connection.send_command('modify cli preference pager disabled display-threshold 0'))
            out_file.write(connection.send_command('show running-config') + '\n\n')
            connection.disconnect()
    except netmiko_exceptions as e:
        print('Failed to ', device['ip'], e)
os.system('sudo mkdir confback 2>>confback.log ')
os.system('sudo mv *.bigip*.cfg confback')
os.system('echo')
os.system('echo "        ****************************************"')
os.system('echo "          all *bigip*.cfg files have been saved in <confback> folder"')
os.system('echo "        ****************************************"')


