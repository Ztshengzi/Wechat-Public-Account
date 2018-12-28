#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 22:56 2017/11/6 

@author: acer
'''
from django.db.models import Q
from blog.models import Post
import json
import copy

def GetBlog(data):
    #web网站主页面
    WebHost='http://blog.yuxuefendou.cn'
    picurl="http://wx.qlogo.cn/mmopen/PiajxSqBRaEJzN7s45KwYMJA4j5kWWfJmzvkicqnA4XD1ibRMPpGTl6Bia8wROhEPZSeEL7AqwY0aYa1fE08NF8I7Q/132"
    q=data
    i = 1
    names = locals()
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).order_by('-id')
    print(len(post_list))
    if len(post_list):
        for post in post_list:
            id = post.id
            excerpt = post.excerpt
            title = post.title
            if i==1:
                str='{"title":"%s","picurl":"%s","description":"%s","url":"%s/post/%s"}'%(title,picurl,excerpt,WebHost,id)
                str = str.replace("\n", "").strip()
                dic = eval(str)
                list=[]
                list.append(dic)
            else:
                str ='{"title":"%s","description":"%s","url":"%s/post/%s"}'%(title,excerpt,WebHost,id)
                str = str.replace("\n", "").strip()
                # dic = eval(str)
                names['dic%s'%i] = eval(str)
                list.append(names['dic%s'%i])
                print(names['dic%s'%i])
                print('\n')
            i=i+1
            if i>=10:
                return list
    else:
        str='{"title": "未找到相关信息","picurl": "%s","description":"请从新输入查询信息","url":"%s"}'%(picurl,WebHost)
        str = str.replace("\n", "").strip()
        dic = eval(str)
        list = [dic]
    return list

