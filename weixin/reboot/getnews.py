#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 21:48 2017/11/8 

@author: acer
'''
picurl="http://wx.qlogo.cn/mmopen/PiajxSqBRaEJzN7s45KwYMJA4j5kWWfJmzvkicqnA4XD1ibRMPpGTl6Bia8wROhEPZSeEL7AqwY0aYa1fE08NF8I7Q/132"
def getNews(dic):
    names = locals()
    i=1
    text = dic['text']
    dic_list=dic['list']
    for new in dic_list:
        article = new['article']
        source = new['source']
        detailurl = new['detailurl']
        print(detailurl)
        if article!='':
            if i==1:
                str='{"title":"%s","picurl":"%s","description":"%s","url":"%s"}'%(article,picurl,article,detailurl)
                str = str.replace("\n", "").strip()
                dic = eval(str)
                list=[]
                list.append(dic)
            else:
                str ='{"title":"%s","description":"%s","url":"%s"}'%(article,article,detailurl)
                str = str.replace("\n", "").strip()
                # dic = eval(str)
                names['dic%s'%i] = eval(str)
                list.append(names['dic%s'%i])
                print(names['dic%s'%i])
                print('\n')
            i=i+1
            if i>8:
                    return list
    return list