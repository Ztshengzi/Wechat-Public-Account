#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 19:24 2017/11/7 

@author: acer
'''
from weixin.models import ParseStation
import requests
import re
def get_parse_station():
    #关闭https证书验证警告
    requests.packages.urllib3.disable_warnings()
    # 12306的城市名和城市代码js文件url
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
    r = requests.get(url,verify=False)
    print(r.text)
    #中文|字母
    pattern = u'@[a-z]+\|([\u4e00-\u9fa5]+)\|([A-Z]+)\|([a-z]+)\|([a-z]+)\|([0-9]+)'
    result = re.findall(pattern,r.text)
    for i in result:
        ParseStation.objects.get_or_create(id=int(i[4]),station=i[0],alias=i[1],fullPingyi=i[2],firstfight=i[3])
    return result
if __name__ == '__main__':
    get_parse_station()