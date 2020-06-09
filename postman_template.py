#!/usr/bin/env python
# coding:utf-8
# author:%(author)s
# time:%(time)s

import json
import requests
import urllib

def %(function_name)s():
    url="%(url)s"
    headers=%(headers)s
    data=%(data)s
    if "Content-Type" in headers.keys():
        if headers["Content-Type"] =="application/json":
            data=json.dumps(data)
        elif headers["Content-Type"] =="application/x-www-form-urlencoded":
            data=urllib.parse.urlencode(data)
    response = requests.%(method)s(url=url, headers=headers, data=data)
    print(response.text)

if __name__=="__main__":
    %(function_name)s()
