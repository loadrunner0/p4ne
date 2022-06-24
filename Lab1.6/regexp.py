#!usr/local/bin/python3
import re
from ipaddress import IPv4Interface
import glob

def ip_check(line):
    # We only need IP addresses and not any mess with numbers and dots
    r = re.match(r'^.+ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', line.lower())
    if r:
        return IPv4Interface(f'{r.group(1)}/{r.group(2)}')

    return None


path = r'C:\Users\ma.gusmanov\Downloads\config_files'
files = glob.glob(rf'{path}\*.txt')
sub = "ip address"
dic = {}

for file in files:
    with open(file) as f:
        for line in f:
            t = ip_check(line)
            if t:
                dic[t.ip] = t.netmask

for key in dic:
    print(f'{key}: {dic[key]}')
