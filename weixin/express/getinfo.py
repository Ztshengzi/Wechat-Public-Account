#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 9:30 2017/11/8 

@author: acer
'''

import json
import urllib
import urllib.request
import hashlib
import base64
import urllib.parse
from weixin.models import Express

# 此处为快递鸟官网申请的帐号和密码
APP_id = "1310991"
APP_key = "a3a25103-80f5-4605-b9f4-57f5b8475568"
DtatType = '2'
url = 'http://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx'

def encrypt(origin_data, appkey):
    """数据内容签名：把(请求内容(未编码)+AppKey)进行MD5加密，然后Base64编码"""
    m = hashlib.md5()
    m.update((origin_data+appkey).encode("utf8"))
    encodestr = m.hexdigest()
    base64_text = base64.b64encode(encodestr.encode(encoding='utf-8'))
    return base64_text


def sendpost(url, datas):
    """发送post请求"""
    postdata = urllib.parse.urlencode(datas).encode('utf-8')
    header = {
        "Accept": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept-Encoding": "utf-8"
    }
    req = urllib.request.Request(url, postdata, header)
    get_data = (urllib.request.urlopen(req).read().decode('utf-8'))
    return get_data

#查询快递公司代码
def get_company(logistic_name):
    """获取对应快递单号的快递公司代码和名称"""
    print(logistic_name)
    obj=Express.objects.filter(name =logistic_name).first()
    if obj:
        return obj.alias
    else:
        return False

def get_traces(logistic_code, shipper_code, appid, appkey, url):
    """查询接口支持按照运单号查询(单个查询)"""
    data1 = {'LogisticCode': logistic_code, 'ShipperCode': shipper_code}
    d1 = json.dumps(data1, sort_keys=True)
    requestdata = encrypt(d1, appkey)
    post_data = {'RequestData': d1, 'EBusinessID': appid, 'RequestType': '1002', 'DataType': '2',
                 'DataSign': requestdata.decode()}
    json_data = sendpost(url, post_data)
    sort_data = json.loads(json_data)
    return sort_data


def recognise(expressname,expresscode):
    """输出数据"""
    # url = 'http://testapi.kdniao.cc:8081/Ebusiness/EbusinessOrderHandle.aspx'
    ShipperCode = get_company(expressname)
    if not ShipperCode:
        redate = '未查到该快递信息,请检查快递单号是否有误！'
    else:
        trace_data = get_traces(expresscode, ShipperCode, APP_id, APP_key, url)
        if trace_data['Success'] == "false" or not any(trace_data['Traces']):
            redate = '未查询到该快递物流轨迹！'
        else:
            str_state = "问题件\n"
            if trace_data['State'] == '2':
                str_state = "在途中\n"
            if trace_data['State'] == '3':
                str_state = "已签收\n"
                redate="目前状态： "+str_state
            trace_data = trace_data['Traces']
            item_no = 1
            for item in trace_data:
                info ="%s\n%s\n\n"%(item['AcceptTime'],item['AcceptStation'])
                redate=redate + info
                item_no += 1
    return redate


def getinfo(text):
    args=text.split(' ')
    expressname = args[0]
    expresscode =args[1]
    str = recognise(expressname,expresscode)
    return str





if __name__ == '__main__':
    code = '1188525996511'
    code = code.strip()
    ShipperCode = 'EMS'
    trace_data = get_traces(code, ShipperCode, APP_id, APP_key, url)
    str=''
    for trace_data in trace_data['Traces']:
        str=''.join(trace_data['AcceptTime']+''+trace_data['AcceptStation'])
        print(str)