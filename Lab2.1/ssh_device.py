#!usr/local/bin/python3

import re
import paramiko
import time


# Parsing a string to find the information we need
def parse_packets(l):
    r = re.search(r'(\d+) packets (.+), (\d+) bytes', l.lower())
    if r:
        key = r.group(2)
        value = f'packets: {r.group(1)}, bytes: {r.group(3)}'
        return f'{key}: {value}'
    return None


BUF_SIZE = 20000
TIMEOUT = 1
host_ip = '10.31.70.209'
login = 'restapi'
password = 'j0sg1280-7@'

# Создаем объект — соединение по ssh
ssh_connection = paramiko.SSHClient()
ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Инициируем соединение по ssh
ssh_connection.connect(host_ip, username=login, password=password, look_for_keys=False, allow_agent=False)
session = ssh_connection.invoke_shell()

session.send("\n")
session.recv(BUF_SIZE)
session.send("terminal length 0\n")
time.sleep(TIMEOUT)

session.send("\n")
session.recv(BUF_SIZE)
session.send("show interface\n")
time.sleep(TIMEOUT*2)
s = session.recv(BUF_SIZE).decode()

# We break the received text into separate lines.
t = s.split('\r\n')

# Loop through each line.
# First we need to find the line with the name of the interface.
# All other lines have a space at the beginning.
length = len(t)
for i in range(length):
    line = t[i]
    if line.startswith(' '):
        continue
    key = line.split(' ')[0]
    i += 1
    if i == length:  # Here is the protection from going out of bounds
        break
    line = t[i]
    # Parse strings until the next string with the interface name is found
    while line.startswith(' '):
        req = parse_packets(line)
        if req:
            print(f'{key} {req}')  # Print result
        i += 1
        line = t[i]


session.close()
