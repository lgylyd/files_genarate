#!/usr/bin/env python
# coding:utf-8
# author:YD
# time:2020/5/25

import time
import json
from pathlib import Path
from log import logger
def main(postman_file_path,postman_dir_path='.',template_file_path='.'):
    """
    :param postman_file_path: postman导出的json文件路径
    :param postman_dir_path: 生成python文件根目录路径
    :param template_file_path: 生成python文件所需模板路径
    :return:
    """
    try:
        #获取json数据
        logger.info("postman导出的文件所在路径：%s"%postman_file_path)
        logger.info("生成python文件所在路径：%s"%postman_dir_path)
        #logger.info("模板所在路径：%s"%template_file_path)
        json_data=postman_json_data(postman_file_path)
        #解析json数据
        dirs_https=postman_dirpaths_httpdatas(json_data)
        logger.info("从json中提取的目录路径和http数据：%s"%dirs_https)
        #生成目录且往生成的文件中写入对应的内容
        data={
            "template_file":template_file_path,
            "file_name":"",
            "change":{
                "author":"YD",
                "time":time.strftime("%Y/%m/%d"),
                "function_name":"",
                "url":"",
                "method":"",
                "headers":{},
                "data":{}
            }
        }
        for dir_http in dirs_https:
            try:
                dir_data=dir_http["name"]
                logger.info("文件名：%s"%dir_data)
                http_data=dir_http["data"]
                #创建文件目录
                create_dir(postman_dir_path+dir_data)
                data["file_name"] = postman_dir_path+dir_data+".py"
                data["change"]["function_name"]="postman_function"
                data["change"]["url"]=http_data["url"]
                data["change"]["method"] = http_data["method"]
                data["change"]["headers"] = http_data["headers"]
                data["change"]["data"] = http_data["data"]
                logger.info("生成文件配置数据：%s"%data)
            except Exception as e:
                logger.error("%s"%repr(e))
            try:
                template_create_file(data)
                logger.info("创建文件%s成功"%data["file_name"])
            except Exception as e:
                logger.error("创建文件%s失败:%s" % (data["file_name"],repr(e)))
    except Exception as e:
        logger.error("%s"%repr(e))
def template_create_file(data):
    """
    通过模版生成文件
    :param data:1.json对象 2.template_file模版文件路径，3.change模版参数数据
    :return:通过模版生成文件
    """
    try:
        template_file=data["template_file"]
        file_name=data["file_name"]
        change=data["change"]
        with open(template_file,"r") as f:
            template_string=f.read()
        file_content=template_string%change
        with open(file_name,"w",encoding="utf-8") as f:
            f.writelines(file_content)
            f.flush()
    except Exception as e:
        logger.error("%s"%str(e))

def postman_json_data(postman_file):
    """
    :param postman_file: postman_file是json文件路径
    :return: json数据
    """
    with open(postman_file,"r",encoding="utf-8") as f:
        file_content=f.read()
    postman_json=json.loads(file_content)
    if not(set(["info","item"]) < set(postman_json.keys())):
        raise Exception("%s非postman导出的json文件"%postman_file)
    return postman_json

def postman_dirpaths_httpdatas(postman_json):
    """
    :param postman_json: postman原始json
    :return: [{"name":"","data":""},....],nane:为目录路径，data:为http请求数据
    """
    dirs_https=[]
    dir_base="//"+postman_json["info"]["name"]
    return (postman_item_dirpaths_httpdatas(postman_json["item"],dirs_https,dir_base))

def postman_item_dirpaths_httpdatas(postman_json_item,dirs_https,dir_base):
    """
    :param postman_json_item: [{'name': 'test1', 'request': 'request1'}, {'item': [{'name': 'test31', 'request': 'request31'}, {'name': 'test32', 'request': 'request32'}, {'name': 'test33', 'request': 'request33'}], 'name': 'test3'},....]
    :param dirs_https:[]
    :param dir_base:""
    :return: [{"name":"","data":""},....],nane:为目录路径，data:为http请求数据
    """
    for i in postman_json_item:
        dir = ""
        dir=dir+dir_base+"//"+i["name"]
        if "item" in i.keys():
            postman_item_dirpaths_httpdatas(i["item"],dirs_https,dir)
        else:
            dir_json={}
            dir_json["name"]=dir
            dir_json["data"]=function_data(i["request"])
            dirs_https.append(dir_json)
    return dirs_https

def function_data(http_data):
    """
    :param http_data: {},提取http请求数据
    :return:
    """
    data={}
    data["url"]=http_data["url"]["raw"]
    data["method"] = http_data["method"].lower()
    data["headers"]={}
    for header in http_data["header"]:
        data["headers"][header["key"]]=header["value"].strip()
    if "body" in http_data.keys():
        data_mode=http_data["body"]["mode"]
        if data_mode == "raw":
            data["data"]=http_data["body"]["raw"]
        elif data_mode == "urlencoded":
            data["data"]={}
            for data_json in http_data["body"]["urlencoded"]:
                data["data"][data_json["key"]]=data_json["value"]
    else:
        data["data"] = {}
    return data

def create_dir(dir_path):
    """
    :param dir_path: "",目录字符串
    :return:
    """
    dir_list=dir_path.split("//")
    dir="//".join(dir_list[0:-1])
    mkdir(dir)

def mkdir(p):
    """
    功能说明：创建指定的目录
    :param p:
    :return:
    """
    try:
        path = Path(p)
        if not path.exists():
            path.mkdir(parents=True)
            # os.makedirs(p)
        else:
            logger.warning("%s已存在"%p)
    except Exception as e:
        logger.error("创建目录%s报错，需要在异常中处理："%p + str(e))
    finally:
        return p

#以下代码是简化前的
def main1(postman_file_path,postman_dir_path='.',template_file_path='.'):
    #生成目录结构
    json_data=postman_json_data(postman_file_path)
    dir_list, http_datas = postman_dirs_http(json_data)
    dir_paths = []
    dir_paths = list_dir_path(dir_list, postman_dir_path, dir_paths)
    mkdirs(dir_paths)
    #往生成的文件中写入对应的内容
    data={
        "template_file":template_file_path,
        "file_name":"",
        "change":{
            "author":"YD",
            "time":time.strftime("%Y/%m/%d"),
            "function_name":"",
            "url":"",
            "method":"",
            "headers":{},
            "data":{}
        }
    }
    for http_data in http_datas:
        for dir_name in dir_paths:
            if http_data["name"] in dir_name:
                data["file_name"] = dir_name+".py"
                continue
        data["change"]["function_name"]="postman_function"
        data["change"]["url"]=http_data["request"]["url"]
        data["change"]["method"] = http_data["request"]["method"]
        data["change"]["headers"] = http_data["request"]["headers"]
        data["change"]["data"] = http_data["request"]["data"]
        print(data)
        template_create_file(data)

def postman_dirs_http(postman_json):
    """
    :param postman_json: json数据
    :return: 1.返回请求名称list路径，2.http请求数据
    """
    dirs = []
    http_data = []
    dirs.append(postman_json["info"]["name"])
    return (postman_item_dirs_http(postman_json["item"], dirs, http_data))

def postman_item_dirs_http(postman_json_item,dirs,http_data):
    """
    :param postman_json_item: postman 中的item数据list
    :param dirs: 存储 文件名目录
    :param http_data: 存储返回数据
    :return:
    """
    for i in postman_json_item:
        dir = []
        dir.append(i["name"])
        if "item" in i.keys():
            postman_item_dirs_http(i["item"],dir,http_data)
        if "request" in i.keys():
            request_data_json={}
            request_data_json["name"]=i["name"]
            request_data_json["request"]=function_data(i["request"])
            http_data.append(request_data_json)
        dirs.append(dir)
    return dirs,http_data

def list_dir_path(dir_list,dir_path,dir_paths):
    if isinstance(dir_list,list):
        dir_path = dir_path
        for i in dir_list:
            if isinstance(i,list):
                list_dir_path(i,dir_path,dir_paths)
                _locator["flag"]=False
            else:
                dir_path=dir_path+"//"+i
                _locator["flag"] = True
        if _locator["flag"]:
            dir_paths.append(dir_path)
    return dir_paths

def mkdirs(p_list):
    for p in p_list:
        print(p)
        p_dirs=p.split("//")
        pj="//".join(p_dirs[0:-1])
        mkdir(pj)
        mktouch(p+".py")

def mktouch(file_name):
    """
    功能说明：创建指定的目录
    :param p:
    :return:
    """
    try:
        path = Path(file_name)
        if not path.exists():
            path.touch()
    except Exception as e:
        print("创建报错，需要在异常中处理：" + str(e))
    finally:
        return file_name

_locator = {
    "flag": True,
    "count":0
}

if __name__=="__main__":
    postman_file_path = "OMS系统.postman_collection.json"
    # postman_json=postman_json_data(postman_file_path)
    # # pdh=postman_dirs_http(postman_json)[0]
    # # requests=postman_dirs_http(postman_json)[1]
    # # print(requests)
    # # print(list_dir_path(pdh,'.',[]))
    # print(postman_dirpaths_httpdatas(postman_json))
    main(postman_file_path, postman_dir_path='.', template_file_path='.//postman_template.py')