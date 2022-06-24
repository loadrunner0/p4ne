#!usr/local/bin/python3
import re
from ipaddress import IPv4Interface
import glob

path = r'C:\Users\ma.gusmanov\Downloads\config_files'
files = glob.glob(rf'{path}\*.txt')
sub = "ip address"
dic = {}

for file in files:
    with open(file) as f:
        for line in f:
            r = re.match(r'^.+ip address ([\d.]+) ([\d.]+)', line.lower())
            if r:
                dic[r.group(1)] = r.group(2)

for key in dic:
    print(f'{key}: {dic[key]}')
