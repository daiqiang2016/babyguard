#!/usr/bin/python
# -*- coding: utf-8 -*-

'''babyguard.URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r\'^$\', views.home, name=\'home\')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r\'^$\', Home.as_view(), name=\'home\')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r\'^blog/\', include(\'blog.urls\'))
'''

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from babyguard.chart import views
urlpatterns = [
    url('^show$', views.show, name='show'), 
    url('^get_video_chart$', views.get_video_chart, name='get_video_chart'), 
    url('^show_video$', views.show_video, name='show_video'), 
    url('^get_audio_chart$', views.get_audio_chart, name='get_audio_chart'), 
    url('^show_audio$', views.show_audio, name='show_audio'), 
    ]
