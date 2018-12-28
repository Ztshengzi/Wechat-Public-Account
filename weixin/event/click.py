#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 22:59 2017/11/9 

@author: acer
'''
from weixin.config import wechat_instance
def response_event():
    EventKey=wechat_instance.message.type