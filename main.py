#!/usr/bin/env python
# coding:utf-8
# author:YD
# time:2020/6/11

import re
class InitParameter():
    operator = "chengzaolin"
    personName = "chengzaolin"
    ticket = "542179b0abed6afc06448604b0a7da95"
    funcVersion = "fc2783c1b1a3baa6e34d408744398108"
    requestId = "051917364451421a0dea57a30acd1960"
    group = "rpc-service-group-test"
    url_test = "http://test.newoms-http-provider.kokoerp.com"
    url = "https://erp-test.youkeshu.com"
    url_wms = "http://test.newwms.kokoerp.com/"

file_name=".//登录oms系统.py"
r = re.compile("{{.*?}}")
with open(file_name, "r", encoding="utf-8") as f:
    file_string = f.read()
arg_list = r.findall(file_string)
for i in arg_list:
    print(i)
    file_string = file_string.replace(i, getattr(InitParameter, i[2:-2]))
with open(file_name, "w", encoding="utf-8") as f:
    f.write(file_string)
    f.flush()
import 登录oms系统 as function_nmae
try:
    function_nmae.postman_function()
except Exception as e:
    print("%s"%str(e))
for i in arg_list:
    file_string = file_string.replace(getattr(InitParameter, i[2:-2]), i)
with open(file_name, "w", encoding="utf-8") as f:
    f.write(file_string)
    f.flush()
