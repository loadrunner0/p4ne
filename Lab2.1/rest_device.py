#!usr/local/bin/python3

import requests
import pprint
import ssl
import urllib3

from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter


class Ssl1HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1)


def get_statistic(interface):
    get = f'{url}/api/v1/interfaces/{interface}/statistics'
    r = s.get(get, headers=header, verify=False)
    if r.status_code == 200:
        in_packets = r.json()['in-total-packets']
        out_packets = r.json()['out-total-packets']
        return f'packets in: {in_packets}, packets out: {out_packets}'
    else:
        return r.status_code


host_ip = '10.31.70.210'
port = '55443'
login = 'restapi'
password = 'j0sg1280-7@'
url = f'https://{host_ip}:{port}'
post = f'{url}/api/v1/auth/token-services'
get = f'{url}/api/v1/interfaces'

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

s = requests.Session()
s.mount(url, Ssl1HttpAdapter())

r = s.post(post, auth=(login, password), verify=False)
token = r.json()['token-id']

header = {"content-type": "application/json", "X-Auth-Token": token}
r = s.get(get, headers=header, verify=False)

if r.status_code == 200:
    for interface in r.json()['items']:
        str = interface['if-name']
        print(f'{str}: {get_statistic(str)}')
else:
    print(r.status_code)

s.close()
