#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 20:48 2017/11/4 

@author: acer
'''

import json
from tuliing import reboot

if __name__ == '__main__':
    test=reboot("新闻")
    # test=test.encode('utf-8')
    # print test
    # print type(test)
    print(type(test))
    dic_json = json.loads(test)
    code=dic_json['code']
    print (code)
    if code == 100000:
        print (dic_json['text'].encode('utf-8').decode('utf-8'))
        # print(dic_json)
    elif code ==200000:
        print  (dic_json['text']+'\n'+dic_json['url'])
    elif code ==300000:
        data=dic_json['text']+'\n'+dic_json['list']
        print (data)

