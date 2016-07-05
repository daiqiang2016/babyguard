# -*- coding: utf-8 -*-

import logging
import json
import random
import sys
import pyUsage

from django.conf.urls import patterns, include, url
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.contrib.auth.tokens import default_token_generator
from django.contrib import admin 
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.wsgi import get_wsgi_application
from django.db import models
from django.db.models import Q
from django.forms import ModelForm
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django import forms
from django import template
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Template, Context
from django.template.loader import get_template
from django.test.client import Client
from django.utils.functional import wraps
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt

from babyguard.account.models import BaseProfileModel
#, ProfileUserModel

###通过id，而不是手机号去唯一标志一个用户
class ProfileManager():
    ###get users--------------------------------------------------------                         
    @staticmethod
    def get_base_profiles():
        base_profiles = BaseProfileModel.objects.all()
        return base_profiles

    @staticmethod
    def get_users():
        profiles = ProfileUserModel.objects.all()
        users = [e.base_profile.user for e in profiles]
        return users

    @staticmethod
    def get_sms_code_by_username(username):
        users = User.objects.filter(username = username)
        if len(users) == 0: return ''
        basic_profile = users[0].base_profile
        if basic_profile is None: return ''
        return basic_profile.sms_code

    @staticmethod
    def get_users_by_user_id(user_id):
        users = User.objects.filter(id = user_id)
        return users
    
    @staticmethod
    def get_users_by_username(username):
        users = User.objects.filter(username = username)
        return users
    
    @staticmethod
    def get_users_by_nickname(nickname):
        profiles = BaseProfileModel.objects.filter(nickname = nickname)
        users = [e.user for e in profiles]
        return users
    
    @staticmethod
    def get_users_by_mobile(mobile):
        ###策略：先返回username，如果没有就返回mobile
        users = User.objects.filter(username = mobile)
        if len(users) != 0: return users
        
        ###返回mobile
        #profiles = BaseProfileModel.objects.filter(mobile = mobile)
        #users = [e.user for e in profiles]
        #if len(users) != 0: return users
        return []
        
    ###user_profile --> profile -->user
    @staticmethod
    def get_users_by_profile(profile):
        return [profile.profile.user,]

    ###get profiles--------------------------------------------------------                         
    @staticmethod
    def get_profiles_by_user_id(user_id):
        users = ProfileManager.get_users_by_user_id(user_id)
        if len(users) == 0:
            return []
        profiles = ProfileManager.get_profiles_by_user(users[0])
        return profiles
        
    @staticmethod
    def get_profiles_by_user(user):
        concrete_profile_id = user.base_profile.concrete_profile_id
        user_type = user.base_profile.user_type
        if user_type == 'USER':
            profiles = ProfileUserModel.objects.filter(id = concrete_profile_id)
            return profiles
        return []    
            
    @staticmethod
    def get_base_profiles_by_username(username):
        users = ProfileManager.get_users_by_username(username)
        if len(users) == 0:
            return []
        basic_profiles = [e.base_profile for e in users]
        return basic_profiles
        
    @staticmethod
    def get_profiles_by_username(username):
        users = ProfileManager.get_users_by_username(username)
        if len(users) == 0:
            return []
        print pyUsage.get_cur_info(), 'users= ', users
        profiles = ProfileManager.get_profiles_by_user(users[0])
        return profiles

    @staticmethod
    def get_profiles_by_nickname(nickname):
        users = ProfileManager.get_users_by_nickname(nickname)
        if len(users) == 0:
            return []
        profiles = ProfileManager.get_profiles_by_user(user[0])
        return profiles
        
    @staticmethod
    def get_profiles_by_mobile(mobile):
        ###获得profiles
        users = ProfileManager.get_users_by_mobile(nickname)
        if len(users) == 0:
            return []
        profiles = ProfileManager.get_profiles_by_user(user[0])
        return profiles

    @staticmethod
    def is_profile_user(user_id):
        profiles = ProfileManager.get_profiles_by_user_id(user_id)
        if len(profiles) == 0:
            return False
        if 'USER' == profiles[0].user_type:
            return True
        return False

    @staticmethod
    def get_base_profile(base_profile):
        profile_info = {}
        profile_info['username'] = base_profile.user.username
        profile_info['login_name'] = base_profile.login_name
        profile_info['user_id']  = base_profile.user.id
        profile_info['nickname'] = base_profile.nickname
        profile_info['mobile']   = base_profile.mobile
        return profile_info

    @staticmethod    
    def get_profile(user):
        base_profile = user.base_profile
        profile_info = {}
        profile_info['username'] = user.username
        profile_info['user_id']   = user.id
        profile_info['nickname'] = base_profile.nickname
        profile_info['mobile']   = base_profile.mobile
        profiles = ProfileManager.get_profiles_by_user(user)
        if len(profiles) > 0:
            profile_info['user_type'] = profiles[0].user_type
            #print 'attr= ', profiles[0].attribute
            ###目前还不知道如何判断属性是否存在
            if 'COMPANY_DETECT' == profile_info['user_type']:
                profile_info['addr_province'] = profiles[0].addr_province
                profile_info['addr_city']     = profiles[0].addr_city
                profile_info['addr_street']   = profiles[0].addr_street
            if 'COMPANY_FIX' == profile_info['user_type']: 
                profile_info['addr_province'] = profiles[0].addr_province
                profile_info['addr_city']     = profiles[0].addr_city
                profile_info['addr_street']   = profiles[0].addr_street
                
        return profile_info

