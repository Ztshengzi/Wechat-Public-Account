#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 20:05 2017/11/4 

@author: acer
'''

from urllib.parse import quote
from urllib.request import urlopen
import json

key = 'f156e99bbc6a43059eafcb3b2e55482e'
# key = '6129b8aafef24c848db29121e845a1cf'
api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

def getHtml(url):
    page = urlopen(url)
    html = page.read().decode('utf-8')
    return html

def reboot(data):
    # print "reboot:"+data
    info = quote(data)
    request = api + info
    print(request)
    response = getHtml(request)

    print(response)
    # print response.decode('utf-8')
    return response
    # dic_json = json.loads(response)
    # print '机器人: '.decode('utf-8') + dic_json['text']
    # code=dic_json['code']
    # print code
    # if code == 100000:
    #     return dic_json['text'].encode('utf-8')
    # elif code ==200000:
    #     data=dic_json['text']+'\n'+dic_json['url']
    #     return data.encode('utf-8')
    # elif code ==300000:
    #     data=dic_json['text']+'\n'+dic_json['list']
    #     return data.encode('utf-8')


if __name__ == '__main__':
    reboot("你好")

