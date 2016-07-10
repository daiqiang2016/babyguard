# -*- coding:utf-8 -*-
import time
import random
import datetime
import pyUsage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.shortcuts import render,render_to_response
from babyguard.account.models import *
from babyguard.account.forms import *
from babyguard.helper import JsonResponse, pack_json_resp
import babyguard.account.sms as sms

def gen_sms_code(username):
    e_list = ProfileModel.objects.filter(username = username)
    if len(e_list) > 0:
        e = e_list[0]
        e.sms_code = '%04d'%( random.randint(0,10000) )
        ret = e.save()
        return ret
    return False

def is_sms_code_equal(username, sms_code):
    e_list = ProfileModel.objects.filter(username = username)
    if len(e_list) > 0:
        e = e_list[0]
        if e.sms_code == sms_code:
            return True
    return False

def is_username_exists(username):
    e_list = ProfileModel.objects.filter(username = username)
    if len(e_list) == 0:
        return False
    return True

def change_password(username, password):
    e_list = ProfileModel.objects.filter(username = username)
    if len(e_list) > 0:
        e = e_list[0] 
        e.password = password
        ret = e.save()
        return ret
    return False

def is_password_valid(username, password):
    e_list = ProfileModel.objects.filter(username = username)
    if len(e_list) > 0:
        e = e_list[0]
        if e.password == password:
            return True
    return False
def update_user(username, password='', sms_code = ''):
    if not is_username_exists(username):
        return False
    e_list = ProfileModel.objects.filter(username = username)
    e = e_list[0]
    e.username = username
    e.password = password
    e.sms_code = sms_code
    ret = e.save()
    return ret

def add_user(username, password, sms_code = ''):
    e = ProfileModel(
          username = username,
          password = password,
          sms_code = sms_code,
    )
    ret = e.save()
    #print pyUsage.get_cur_info(), 'ret= ', ret
    return ret
def append_history(username, video_id):
    e = HistoryModel(
        username = username,
        video_id = video_id,
    )
    ret = e.save()
    return ret
    
def append_collect(username, video_id):
    e = HistoryModel(
        username = username,
        video_id = video_id,
    )
    ret = e.save()
    return ret

@csrf_exempt
def add_device(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        device = request.POST.get('device')
        if not is_username_exists(username):
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        objs = ProfileModel.objects.filter(username = username)
        assert(len(objs) == 1)
        
        obj = objs[0]
        obj.device = device
        ret = obj.save()
        return pack_json_resp(ret, 'add_device error', -1)
    else:
        pass
    form = DeviceForm(
        initial={
            'username':'18684016495',
            'device':'test',
        }
    ) 
    return render_to_response('device.html', {'form':form})

@csrf_exempt
def add_history(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        video_id = request.POST.get('video_id')
        ret = append_history(username, video_id)
        return pack_json_resp(ret, 'add_history error', -1)
    else:
        pass
    form = HistoryForm(
        initial={
            'username':'18684016495',
            'video_id':'test',
        }
    ) 
    return render_to_response('history.html', {'form':form})
    
@csrf_exempt
def add_collect(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        video_id = request.POST.get('video_id')
        ret = append_collect(username, video_id)
        return pack_json_resp(ret, 'add_collect error', -1)
    else:
        pass
    form = CollectForm(
        initial={
            'username':'18684016495',
            'video_id':'test',
        }
    ) 
    return render_to_response('collect.html', {'form':form})
        
@csrf_exempt
def clear_all_users(request):
    e_list = ProfileModel.objects.all()
    pre_cnt = len(e_list)
    for e in e_list:
        e.delete()
    e_list = ProfileModel.objects.all()
    cur_cnt = len(e_list)    
    return JsonResponse(
    {
        'status':'success',
        'status_code':0,
        'pre_cnt':pre_cnt,
        'cur_cnt':cur_cnt,
    })
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not is_username_exists(username):
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if not is_password_valid(username, password):
            return pack_json_resp(False, 'password wrong', -1)

        return pack_json_resp(True, 'login ok', 0)
    else:
        pass
    form = ProfileForm(
            initial={
                'username':'test',
                'password':'test',
            }
    )   
    user_list = []
    e_list = ProfileModel.objects.all()
    for e in e_list:
        d = {}
        d['username'] = e.username
        d['password'] = e.password
        user_list.append(d)
    return render_to_response('login.html', {'form':form, 'user_list':user_list}) 
@csrf_exempt
def modify_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        if not is_username_exists(username):
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if not is_password_valid(username, password):
            return pack_json_resp(False, 'password wrong', -1)
        ret = change_password(username, new_password)
        if ret == True:
            return pack_json_resp(True, 'modify_password ok', 0)

        return pack_json_resp(False, 'modify_password error', -1)
    else:
        pass
    form = ModifyPasswordForm(
        initial={
            'username':'18684016495',
            'password':'test',
            'new_password':'test2',
        }
    )
    return render_to_response('modify_password.html', {'form':form}) 
    
@csrf_exempt
def send_sms(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not is_username_exists(username):
            add_user(username, password = '')
            #return JsonResponse({
            #    'status':'not exists',
            #    'status_code':-1,
            #})
        ret = gen_sms_code(username)
        #print pyUsage.get_cur_info(), 'ret= ', ret
        if ret != True:
            return pack_json_resp(False, 'gen_sms_code error', -1)
            
        objs = ProfileModel.objects.filter(username = username)
        assert(len(objs) == 1)
        
        obj = objs[0]
        ret_json = sms.send_sms(username, obj.sms_code)
        flag = ret_json['code']
        return pack_json_resp(flag, ret_json['msg'], ret_json['code'])
    else:
        pass
    form = ProfileForm(
            initial={
                'username':'18684016495',
            }
    )   
    return render_to_response('send_sms.html', {'form':form})          

@csrf_exempt
def register_app_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not is_username_exists(username):
            ret = add_user(username, password)
            
        if is_username_exists(username):
            return pack_json_resp(True, 'register_app_user ok', 0)
    else:
        pass
    form = ProfileForm(
        initial={
            'username':'test',
            'password':'test',
        }
    ) 
    return render_to_response('register.html', {'form':form})
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        sms_code = request.POST.get('sms_code')
        if not is_username_exists(username):
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if not is_sms_code_equal(username, sms_code):
            return pack_json_resp(False, 'sms_code not equal', -1)
        ret = change_password(username, password)           
        return pack_json_resp(ret, 'register_app_user error', 0)
        
    else:
        pass
    form = ResetPasswordForm(
            initial={
                'username':'test',
                'password':'test',
            }
    )   
    return render_to_response('reset_password.html', {'form':form})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        sms_code = request.POST.get('sms_code')
        if not is_username_exists(username):
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if len(password) == 0:
            return pack_json_resp(False, 'password is empty', -1)

        objs = ProfileModel.objects.filter(username = username)
        ###通过判断password是否为空确定是否注册过
        obj = objs[0]
        if len(obj.password) != 0:
            return pack_json_resp(False, '[%s]exists'%username, -1)

        if sms_code == obj.sms_code:
            obj.password = password
            ret = obj.save()
            return pack_json_resp(ret, 'password save error', -1)
        return pack_json_resp(False, 'register error', -1)
    else:
        pass
    form = RegisterForm(
            initial={
                'username':'18684016495',
                'password':'',
                'sms_code':'',
            }
    )   
    user_list = []
    e_list = ProfileModel.objects.all()
    print ('e_list= ', e_list)
    for e in e_list:
        if e is None:
            continue
        d = {}
        d['username'] = e.username
        d['password'] = e.password
        d['sms_code'] = e.sms_code
        user_list.append(d)
    #print pyUsage.get_cur_info(), 'user_list= ', user_list    
    return render_to_response('register.html', {'form':form, 'user_list':user_list}) 


