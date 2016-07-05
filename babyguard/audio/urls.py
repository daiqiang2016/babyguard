#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
import babyguard.audio.views as views

urlpatterns = [
    url('add_audio$', views.add_audio, name='add_audio'),
    url('get_audio$', views.get_audio, name='get_audio'),
    url('del_audio$', views.del_audio, name='del_audio'),
    url('update_audio$', views.update_audio, name='update_audio'),
    url('reset_all_audio$', views.reset_all_audio, name='reset_all_audio'),
    url('add_comment$', views.add_comment, name='add_comment'),

    #url('get_user_by_user_id$',views.get_user_by_user_id, name='get_user_by_user_id'), 
    #url('login$', views.login, name='login'), 
    #url('modify_password$', views.modify_password, name='modify_password'), 
    #url('modify_user_info$', views.modify_user_info, name='modify_user_info'), 
    #url('register$', views.register, name='register'), 
    #url('register_app_user$', views.register_app_user, name='register_app_user'), 
    #url('reset_password$', views.reset_password, name='reset_password'), 
    #url('send_sms$', views.send_sms, name='send_sms'), 
    #url('clear_all_users$', views.clear_all_users, name='clear_all_users'),
    #url('^test$', views.test, name='test'), 
]
