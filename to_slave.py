#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 9:12 2018/4/25 

@author: acer
'''
from django.contrib.contenttypes.models import ContentType

def run():

    def  do(Table):
        if Table is not None:
            table_objects = Table.objects.all()
            for i in table_objects:
                i.save(using='slave')

    ContentType.objects.using('slave').all().delete()

    for i in ContentType.objects.all():
        do(i.model_class())