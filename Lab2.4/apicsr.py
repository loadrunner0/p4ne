#!usr/local/bin/python3

from flask import Flask, jsonify
import requests
import ssl
import json

from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter


class Ssl1HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def authorize():
    host_ip = '10.31.70.210'
    port = '55443'
    login = 'restapi'
    password = 'j0sg1280-7@'
    url = f'https://{host_ip}:{port}'
    post = f'{url}/api/v1/auth/token-services'
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
    s = requests.Session()
    s.mount(url, Ssl1HttpAdapter())
    r = s.post(post, auth=(login, password), verify=False)
    if r.status_code == 200:
        token = r.json()['token-id']
        header = {"content-type": "application/json", "X-Auth-Token": token}
        get = f'{url}/api/v1/global/memory/processes'
        r = s.get(get, headers=header, verify=False)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    else:
        return None


def get_result(json_list, count=10):
    json_list.sort(key=lambda x: x['memory-used'], reverse=True)
    result = '<a href="/">To start page</a><br><br>'
    i = 0
    for k in json_list:
        if i < count:
            result += f"{k['process-name']}: {k['memory-used']}<br>"
            i += 1
        else:
            return result
    return result


app = Flask(__name__)


@app.route('/')
def index():
    result = '<a href="/memory">Show processes list</a>'
    return result


@app.route('/memory')
def get_processes():
    result = authorize()
    if result:
        l = get_result(result['processes'])
        return l


if __name__ == '__main__':
    app.run(debug=True)
