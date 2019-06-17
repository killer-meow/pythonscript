# Monday, 17 June 2019
# Author:nianhua
# Blog:https://github.com/nian-hua/


import requests
import re


def show_requests(r):

    content = ''

    method = r.request.method
    path_url = r.request.path_url
    content += method + ' ' + path_url + ' HTTP/1.1' + '\n'
    host = re.findall(r'[https://,http://](.*?)/', r.request.url)
    content += 'Host: ' + host[1] + '\n'
    for i in r.request.headers:
        content += i + ':' + r.request.headers[i] + '\n'
    content += '\n' + r.request.body + '\n'

    return content


payload = {'some': 'data'}

r = requests.post('https://www.apple.com',
                  data=payload, allow_redirects=False)

print show_requests(r)
