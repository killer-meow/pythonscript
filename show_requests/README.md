
##用来显示requests发送的数据包
</br>
例如:
```
POST / HTTP/1.1
Host: www.apple.com
Connection:keep-alive
Accept-Encoding:gzip, deflate
Accept:*/*
User-Agent:python-requests/2.20.0
Content-Length:9
Content-Type:application/x-www-form-urlencoded

some=data
```
大佬还介绍了另一种方法:
```
import requests
from requests_toolbelt.utils import dump
resp = requests.get('https://httpbin.org/redirect/5')
data = dump.dump_all(resp)
print(data.decode('utf-8'))
```
