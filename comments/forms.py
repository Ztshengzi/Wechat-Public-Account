#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 23:04 2017/9/14 

@author: acer
'''

# from django import forms
# from .models import Comment
#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['name', 'email', 'url', 'text']

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']