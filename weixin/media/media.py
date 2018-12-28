#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 15:12 2017/11/9 

@author: acer
'''
from weixin.config import wechat_instance

def upload_media(media_type, media_file, extension=''):
    wechat_instance.upload_media(media_type,media_file,extension='')