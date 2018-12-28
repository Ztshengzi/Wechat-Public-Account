#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 21:56 2017/11/6 

@author: acer
'''
from ..reboot.tuliing import reboot
import json
from ..config import wechat_instance
from .getblog import GetBlog
from weixin.get12306.get12306 import GetInfoTrain,get_query_url
from weixin.express.getinfo import getinfo
from weixin.reboot.getnews import getNews
from weixin.reboot.getlink import getLink,getCookBook
from weixin.user.usermange import sendinfo
def response_text(data,flag):
    content = data.strip()
    if content == '功能':
        reply_text = (
            '目前支持的功能：\n1. 关键词前面面加上【博客】两个字可以搜索教程，'
            '\n比如回复 博客 "Django 后台"\n'
            '2.关键词前面面加上【火车票】三个字可以搜索火车票，格式：火车票 时间 出发点 目的地'
            '\n比如回复 火车票 2017-11-7 北京 上海\n'
            '3.关键词前面面加上【快递】三个字可以搜索物流信息，格式：快递 快递名称 快递单号'
            '\n比如回复 快递 邮政 123456\n'
            '4. 回复任意词语，查天气，陪聊天，讲故事，无所不能！\n'
            
            '还有更多功能正在开发中哦 ^_^\n'
            '【<a href="http://blog.yuxuefendou.cn/post/19/">详细介绍</a>】'
        )
    # elif content.endswith('博客'):
    elif content[:2]=='博客':
        #截取后两位博客并去除尾部空格
        content=content[2:].strip()
        list=GetBlog(content)
        # print(type(list))
        # reply_text = '您要找的教程如下：'
        # str = json.dumps(str)
        return wechat_instance.response_news(list)
    elif content[:3]=='火车票':
        content=content[3:].strip()
        url=get_query_url(content)
        tain_info=content.split(' ')
        info_list_dic = GetInfoTrain(url,False)
        info_list = info_list_dic['train_info_list']
        status = info_list_dic['status']
        info = info_list_dic['info']
        url = "\"http://blog.yuxuefendou.cn/train/?time="+tain_info[0]+'&place='+tain_info[1]+'&destination='+tain_info[2]+"\""
        if status==1:
            reply_text = ('本次查询共获取%s趟信息，由于微信文本长度限制，只能回复时间最新的5条列车信息\n\n' % len(info_list) + ''.join(
                info_list[0:5]) + "【<a href=" + url + ">详细信息</a>】")
        else:
            reply_text = (info + "【<a href=" + url + ">详细信息</a>】")

        print(reply_text)
    elif content[:2]=='快递':
        content=content[2:].strip()
        reply_text=getinfo(content)
    else:
        rebootdata = reboot(content)
        dic_json = json.loads(rebootdata)
        code = dic_json['code']
        if code == 100000:
            reply_text = dic_json['text']
        elif code == 200000:
          list=getLink(dic_json,content)
          return wechat_instance.response_news(list)
        elif code == 302000:
            list=getNews(dic_json)
            return wechat_instance.response_news(list)
        elif code == 308000:
            list = getCookBook(dic_json)
            return wechat_instance.response_news(list)
        else:
            reply_text='没有找打您需要的'
    str = "您语音输入的为:%s\n\n" % data
    if flag:
        reply_text=str + reply_text
    return reply_text,wechat_instance.response_text(content=reply_text)
