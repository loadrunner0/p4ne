#!usr/local/bin/python3

import glob

path = r'C:\Users\ma.gusmanov\Downloads\config_files'
files = glob.glob(rf'{path}\*.txt')
sub = "ip address"
dic = {}

for file in files:
    with open(file) as f:
        for line in f:
            # We are looking for the desired string, case insensitive
            l = line.lower()
            ind = l.find(sub)
            if ind != -1:
                # Truncate the string and create a temporary array
                # that will contain our ip and mask at indexes 2 and 3
                temp = l[ind: len(l) - 1].split(' ')
                if len(temp) > 3:
                    ip = temp[2]
                    mask = temp[3]
                    dic[ip] = mask # We only need unique IPs

for key in dic:
    print(f'{key}: {dic[key]}')
