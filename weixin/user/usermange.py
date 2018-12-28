#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 15:30 2017/11/9 

@author: acer
'''
from weixin.config import wechat_instance
from weixin.models import UserInfo,UserLocation,DialogueInformation
import time

"""
:param SaveUser() 初始化用户数据保存至数据库中
:param SaveUserInfo() 初始化用户详细信息
:param SaveUser(openid) 关注用户数据保存至数据库中，存在不处理，不存在添加至数据库
:param SaveUserInfo(openid) 关注用户详细信息保存，之前关注过修改关注状态
"""


def UpdateUserInfo(openid):
    obj = UserInfo.objects.filter(openid=openid)
    if obj:
        obj.update(subscribe=1)
    else:
        info = wechat_instance.get_user_info(openid,lang='zh_CN')
        print(info)
        subscribe_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info['subscribe_time']))
        UserInfo.objects.create(openid=openid, headimgurl=info['headimgurl'],
                                subscribe_time=subscribe_time,
                                sex=info['sex'], language=info['language'],
                                subscribe=info['subscribe'], province=info['province'],
                                nickname=info['nickname'], country=info['country'],
                                groupid=info['groupid'], remark=info['remark'],
                                city=info['city'])


def DelUser(openid):
    UserInfo.objects.filter(openid=openid).update(subscribe=2)


def UpdateUser():
    """
    更新系统中用户系统，如果如何不存在则添加用户信息
    若系统中存在用户，这更新用户相关信息
    :param openidlist 保存获取到的所有用户列表
    :param obj  User  moudle
    :param info 用户详细信息
    """
    openidlist =wechat_instance.get_followers()
    for openid in openidlist['data']['openid']:
        info = wechat_instance.get_user_info(openid, lang='zh_CN')
        obj = UserInfo.objects.filter(openid=openid)
        subscribe_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info['subscribe_time']))
        print("已经判读了obj")
        if not obj:
            print("进入添加区")
            UserInfo.objects.create(openid=openid, headimgurl=info['headimgurl'],
                                    subscribe_time=subscribe_time,
                                    sex=info['sex'], language=info['language'],
                                    subscribe=info['subscribe'], province=info['province'],
                                    nickname=info['nickname'], country=info['country'],
                                    groupid=info['groupid'], remark=info['remark'],
                                    city=info['city'])
        else:
            print('进入修改区域')
            obj.update(headimgurl=info['headimgurl'],
                                    subscribe_time=subscribe_time,
                                    sex=info['sex'], language=info['language'],
                                    subscribe=info['subscribe'], province=info['province'],
                                    nickname=info['nickname'], country=info['country'],
                                    groupid=info['groupid'], remark=info['remark'],
                                    city=info['city'])



def sendinfo(user,text):
        #wechat_instance.send_text_message(user_id='o1rJcwU25DmE5ow_evPqKUZ7YqP0',content="test")
        wechat_instance.send_text_message(user_id=user,content=text)


def SaveUserLocation(userId,Latitude,Longitude):
    print(userId,Latitude,Longitude)
    userinfo = UserInfo.objects.filter(openid=userId).first()
    UserLocation.objects.create(user=userinfo,Latitude=Latitude,Longitude=Longitude)


def SaveContent(openid,MSgType,receiveTime,receiveContent,sendContent):
    print(openid,MSgType,receiveTime,receiveContent,sendContent)
    receiveTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(receiveTime))
    userinfo = UserInfo.objects.filter(openid=openid).first()
    DialogueInformation.objects.create(user=userinfo,MSgType=MSgType,receiveTime=receiveTime,receiveContent=receiveContent,sendContent=sendContent)

if __name__ == '__main__':
    def test():
        x=wechat_instance.get_followers()
        print(x)
        for user in x['data']['openid']:
            user =wechat_instance.get_user_info(user,lang='zh_CN')
            print(user)

    def test1(openid):
        info = wechat_instance.get_user_info(openid, lang='zh_CN')
        print(info)