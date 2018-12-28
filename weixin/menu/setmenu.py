#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 14:26 2017/11/9 

@author: acer
'''
from weixin.config import wechat_instance

def setMenu():
    dict=(
        {
            'button': [
                {
                    'type': 'click',
                    'name': '功能介绍',
                    'key': 'Introduction'
                },
                {
                    'type': 'view',
                    'name': '火车票查询',
                    'url': 'http://xukang.yuxuefendou.cn/train'
                },

                {
                    'name': '菜单',
                    'sub_button': [

                        {
                            'type': 'view',
                            'name': '我的博客',
                            'url': 'http://blog.yuxuefendou.cn/'
                        },
                        {
                            'type': 'view',
                            'name': '搜索',
                            'url': 'http://www.baidu.com/'
                        },
                        {
                            'type': 'location_select',
                            'name': '位置',
                            'key': 'rselfmenu_2_0'
                        },
                        {
                            'type': 'pic_photo_or_album',
                            'name': '拍照或者相册发图',
                            'key': 'rselfmenu_1_1'
                        }
                    ]
                }
            ]
        }
    )

    wechat_instance.create_menu(dict)

def getMenu():
    json = wechat_instance.get_menu()
    print(json)
def delMenu():
    json = wechat_instance.delete_menu()
    print(json)
if __name__ == '__main__':
    # x = setMenu()
    # print(x)
    X=getMenu()
    print(X)
    # delMenu()