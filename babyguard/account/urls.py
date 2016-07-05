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
from babyguard.account import views
urlpatterns = [
    #url('get_user_by_user_id$',views.get_user_by_user_id, name='get_user_by_user_id'), 
    url('login$', views.login, name='login'), 
    url('modify_password$', views.modify_password, name='modify_password'), 
    url('register$', views.register, name='register'), 
    #url('modify_user_info$', views.modify_user_info, name='modify_user_info'), 
    url('register_app_user$', views.register_app_user, name='register_app_user'), 
    url('reset_password$', views.reset_password, name='reset_password'), 
    url('send_sms$', views.send_sms, name='send_sms'), 
    url('clear_all_users$', views.clear_all_users, name='clear_all_users'),
    #url('^test$', views.test, name='test'), 
    url('add_history$', views.add_history, name='add_history'),
    url('add_collect$', views.add_collect, name='add_collect'),
    url('add_device$', views.add_device, name='add_device'),
    ]
