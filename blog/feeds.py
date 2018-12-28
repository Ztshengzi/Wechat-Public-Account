#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 19:42 2017/9/16 

@author: acer
'''
from django.contrib.syndication.views import Feed

from .models import Post


class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = "浴血奋斗博客"

    # 通过聚合阅读器跳转到网站的地址
    link = "http://xukang.yuxuefendou.cn:8080/"

    # 显示在聚合阅读器上的描述信息
    description = "浴血奋斗博客文章"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body