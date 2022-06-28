#!usr/local/bin/python3

from flask import Flask, jsonify
import sys
import glob
import re

path = r'C:\Users\ma.gusmanov\Downloads\config_files'
sub_host = 'hostname'
sub_ip = 'ip address'
host_list = []
dic = {}


def get_hostname(text):
    search_host = rf'{sub_host} ([a-zA-Z\-\d]+)'
    r = re.search(search_host, text)
    if r:
        return r.group(1)
    else:
        return None


def collect_hosts():
    files = glob.glob(rf'{path}\*.txt')
    for file in files:
        with open(file) as f:
            h = get_hostname(f.read())
            if h:
                host_list.append(h)


def print_list():
    result = '<a href="/">To start page</a><br><br>'
    for l in host_list:
        result += f'<a href="/configs/{l}">{l}</a><br>'
    return result


def ip_check(line):
    # We only need IP addresses and not any mess with numbers and dots
    r = re.search(rf'{sub_ip} (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', line.lower())
    if r:
        return f'{r.group(1)}/{r.group(2)}'
    else:
        return None


def collect_ip():
    files = glob.glob(rf'{path}\*.txt')
    i = 0
    for file in files:
        host = host_list[i]
        with open(file) as f:
            list_h = []
            for line in f:
                t = ip_check(line)
                if t:
                    list_h.append(t)
        dic[host] = list_h
        i += 1


def print_net(hostname):
    result = '<a href="/">To start page</a><br><br>'
    result += '<a href="/configs">To configs</a><br><br>'
    result += f'List of ip addresses for the host {hostname}:<br>'
    for l in dic[hostname]:
        result += f'{l}<br>'
    return result


app = Flask(__name__)


@app.route('/')
def index():
    result = '<a href="/configs">Show interface list</a>'
    return result


@app.route('/configs')
def p_configs():
    if len(host_list) > 0:
        return print_list()
    else:
        return 'Empty'


@app.route('/configs/<hostname>')
def p_page2(hostname):
    return print_net(hostname)


collect_hosts()
collect_ip()


if __name__ == '__main__':
    app.run(debug=True)
