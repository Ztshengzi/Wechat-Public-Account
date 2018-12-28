from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage,
                                 VideoMessage, LinkMessage, LocationMessage, EventMessage,
                                 )

from weixin.blog.response_text import response_text

from weixin.user.usermange import SaveUserLocation, UpdateUserInfo, DelUser, SaveContent

# 实例化 WechatBasic
from .config import wechat_instance




@csrf_exempt
def index(request):
    if request.method == 'GET':
        """
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        """
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")
    """
    # POST
    # 解析本次请求的 XML 数据
    """

    try:
        wechat_instance.parse_data(data=request.body)
        # 使用str() 将字节数据转换为字符数据并打印
        print(str(request.body, 'utf-8'))
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
    # 利用本次请求中的用户OpenID来初始化上下文对话
    response = None
    # 文本消息处理
    if isinstance(message, TextMessage):
        """
        # step = context.get('step', 1)  # 当前对话次数，如果没有则返回 1
        # last_text = context.get('last_text')  # 上次对话内容
        #获取当前请求数据
        :parameter response_text调用文本处理功能 返回response所需数据
        """
        user_content = message.content  # 当前会话内容
        reply_text,response = response_text(user_content, False)
        print(response)
        SaveContent(message.source,'text',message.time,message.content,reply_text)
        return HttpResponse(response, content_type="application/xml")

    elif isinstance(message, VoiceMessage):
        recognition = wechat_instance.message.recognition
        if recognition:
            reply_text,response = response_text(recognition, True)
            SaveContent(message.source,'voice',message.time,message.media_id,reply_text)
            return HttpResponse(response, content_type="application/xml")
        else:
            reply_text = '你输入的语音没有任何内容，请输入有效语音!'
            SaveContent(message.source,'voice',message.time,message.media_id,reply_text)
    elif isinstance(message, ImageMessage):
        picurl = wechat_instance.message.picurl  # 对应于 XML 中的 PicUrl
        media_id = wechat_instance.message.media_id  # 对应于 XML 中的 MediaId
        response = wechat_instance.response_image(media_id=media_id)
        SaveContent(message.source,'image',message.time,message.media_id,media_id)
        return HttpResponse(response, content_type="application/xml")

    elif isinstance(message, VideoMessage):
        reply_text = '视频我不会看/:P-('
        SaveContent(message.source,'video',message.time,request.body,reply_text)
    elif isinstance(message, LinkMessage):
        reply_text = '链接信息'
        SaveContent(message.source,'video',message.time,request.body,reply_text)
    elif isinstance(message, LocationMessage):
        location = wechat_instance.message.location  # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
        label = wechat_instance.message.label  # 对应于 XML 中的 Label

        # 获取用户位置信息及经纬度数据反馈给用户
        reply_text = "位置：%s\n经纬度：%s" % (label, location)

    elif isinstance(message, EventMessage):  # 事件信息
        if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            UpdateUserInfo(message.source)
            reply_text = '欢迎关注:\n可输入"功能"进行功能查看'

            # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
            if message.key and message.ticket:
                reply_text += '\n来源：扫描二维码关注'
            else:
                reply_text += '\n来源：搜索名称关注'
        elif message.type == 'unsubscribe':
            DelUser(wechat_instance.message.source)
            reply_text = '取消关注事件'
        elif message.type == 'scan':
            reply_text = '已关注用户扫描二维码！'
        elif message.type == 'location':
            SaveUserLocation(message.source, message.latitude, message.longitude)
            reply_text = False
        elif message.type == 'click':

            reply_text = (
                '目前支持的功能：\n1. 关键词前面面加上【博客】两个字可以搜索教程，'
                '\n比如回复 博客 "Django 后台"\n'
                '2.关键词前面面加上【火车票】三个字可以搜索火车票，格式：火车票 时间 出发点 目的地'
                '\n比如回复 火车票 2017-11-7 北京 上海\n'
                '3.关键词前面面加上【快递】三个字可以搜索物流信息，格式：快递 快递名称 快递单号'
                '\n比如回复 快递 邮政 123456\n'
                '4. 回复任意词语，查天气，陪聊天，讲故事，无所不能！\n'

                '还有更多功能正在开发中哦 ^_^\n'
                '【<a href="http://blog.yuxuefendou.cn/post/19/">功能介绍</a>】'
            )
        elif message.type == 'view':
            reply_text = '自定义菜单跳转链接'
        elif message.type == 'templatesendjobfinish':
            reply_text = '模板消息'
    if reply_text:
        response = wechat_instance.response_text(content=reply_text)
    else:
        response = ""
    return HttpResponse(response, content_type="application/xml")




