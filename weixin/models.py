from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

# from __future__ import unicode_literals
#
class ParseStation(models.Model):
    id = models.IntegerField(primary_key=True)
    station = models.CharField(max_length=32, db_index=True)
    alias = models.CharField(max_length=12)
    fullPingyi = models.CharField(max_length=32, db_index=True)
    firstfight = models.CharField(max_length=8, db_index=True)

    def __str__(self):
        return self.station


class Express(models.Model):
    """
    快递查询信息
    """
    name = models.CharField(
        '快递名称', max_length=128, help_text='快递'
    )
    alias = models.CharField(
        '别名', max_length=32, help_text='别名'
    )


class UserInfo(models.Model):
    """
    关注用户信息
    """
    SUBSCIBE = ((1, '已关注'),
                (2, '未关注'),)
    SEX = (
        (1, '男'),
        (2, '女')
    )
    openid = models.CharField(
        '微信号', max_length=128
    )
    country = models.CharField(
        '国家', max_length=36, blank=True
    )
    language = models.CharField(
        '语言', max_length=36, blank=True
    )
    province = models.CharField(
        '省', max_length=36, blank=True
    )
    city = models.CharField(
        '城市', max_length=128, blank=True
    )
    subscribe = models.IntegerField('是否关注', choices=SUBSCIBE)

    subscribe_time = models.DateTimeField(
        '关注时间', blank=True
    )
    groupid = models.IntegerField(
        '分组id', blank=True
    )
    sex = models.IntegerField(
        '性别', choices=SEX
    )
    nickname = models.CharField(
        '别名', max_length=128, blank=True
    )
    remark = models.CharField(
        '备注', max_length=128, blank=True
    )
    headimgurl = models.CharField(
        '用户头像', max_length=256, blank=True
    )

    def __str__(self):
        if self.remark:
            return self.remark
        return self.nickname


class UserLocation(models.Model):
    """
    用户地位位置信息上传
    """
    user = models.ForeignKey(UserInfo)
    Latitude = models.CharField('纬度', max_length=12)
    Longitude = models.CharField('经度', max_length=12)
    createTime = models.DateTimeField('时间', auto_now_add=True)


class DialogueInformation(models.Model):
    """
    用户对话信息
    """
    user = models.ForeignKey(UserInfo)
    MSgType = models.CharField('消息类型',max_length=128)
    receiveTime = models.DateTimeField('接收时间')
    receiveContent = RichTextUploadingField('接收内容', blank=True)
    sendTime = models.DateTimeField('处理时间', auto_now_add=True)
    sendContent = RichTextUploadingField('处理内容', blank=True)

    def __str__(self):
        return self.user
