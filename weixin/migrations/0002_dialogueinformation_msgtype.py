# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-18 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogueinformation',
            name='MSgType',
            field=models.CharField(default=1, max_length=128, verbose_name='消息类型'),
            preserve_default=False,
        ),
    ]
