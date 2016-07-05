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
from babyguard.lab import views
urlpatterns = [
    #url('get_user_by_user_id$',views.get_user_by_user_id, name='get_user_by_user_id'), 
    url('^auth$', views.auth, name='auth'), 
    url('^test$', views.test, name='test'), 
    url('^up_pic$', views.up_pic, name='up_pic'),
    ]
