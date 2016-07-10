from django.shortcuts import render
# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
import pyUsage
import pyIO
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.shortcuts import render,render_to_response
#from babyguard.request_check import *
from urllib.parse import unquote
import json
import hashlib   
#import tencentyun
from babyguard.sns.forms import *
from babyguard.sns.models import *
from babyguard.helper import JsonResponse, pack_json_resp,get_md5
from util import util_log

g_sns_fields = [e.name for e in SnsModel().fields]
g_comment_fields=[e.name for e in CommentModel().fields]

def append_sns(sns_id, url, title, types, duration):
    e = SnsModel(
          sns_id = sns_id,
          url = url,
          title = title, 
          types = types,
          duration = duration)
    ret = e.save()
    print (pyUsage.get_cur_info(), 'ret= ', ret)
    resp = pack_json_resp(ret, 'append_sns err', -1)
    return resp

def objs2dict_list(objs, fields):
    d_list = []
    for obj in objs:
        d = {}
        #print (pyUsage.get_cur_info(), fields)
        for name in fields:
            d[name] = getattr(obj, name)
            #print (pyUsage.get_cur_info(), 'name,v=', name, d[name])
            if isinstance(d[name], datetime.datetime):
                t = d[name].strftime('%Y-%m-%d')
                d[name] = t
            else:    
                pass
                #print (pyUsage.get_cur_info(), type(d[name]) )
        d_list.append(d)
    return d_list

def show_all_fields(e):
    #print pyUsage.get_cur_info(), 'e= ', dir(e)
    #print pyUsage.get_cur_info(), 'e= ', e.fields
    for name in g_sns_fields:
        pass
        #print pyUsage.get_cur_info(), dir(name),type(name)
        #print pyUsage.get_cur_info(), 'name= ', name
        #print pyUsage.get_cur_info(), 'k,v=',name, getattr(name, '__str__')

def update_all_fields(e, val_dict):
    for name in g_sns_fields:
        v = val_dict.get(name,'')
        if len(v) != 0:
            setattr(e, name, v)
    ret = e.save()
    return ret

@csrf_exempt
def reset_all_sns(request):
    e_list = SnsModel.objects.all()
    for e in e_list:
        e.delete()

    #f = '/data/babyguard/babyguard/babyguard/sns/all_sns.txt'
    f = os.path.split(os.path.realpath(__file__))[0] + '/all_sns.txt'
    t_list = pyIO.read_file_content(f, 'utf-8')
    for t in t_list:
        #print pyUsage.get_cur_info(), 't= ', t
        t = t.strip()
        if t.find('http://') == -1:
            continue

        arr = t.split('\t')
        if len(arr) < 4:
            continue
        
        arr = t.split('\t')
        sns_id = get_md5(arr[0])
        url = arr[0]
        title = arr[1]
        types = arr[2]
        duration = arr[3]
        ret = append_sns(sns_id, url, title, types, duration)       
        print (pyUsage.get_cur_info(), 'add ret= ', ret)

    objs = SnsModel.objects.all()
    #print pyUsage.get_cur_info(), 'cnt= ', len(objs)
    sns_list = objs2dict_list(objs, g_sns_fields)
    #print pyUsage.get_cur_info(), 'cnt= ', len(sns_list)

    return JsonResponse(
            {
                'status': 'reset sns',
                'status_code':0,
                'cnt':len(sns_list),
                'sns_list':sns_list,
             })
    #print pyUsage.get_cur_info(), 'add ret= ', ret

@csrf_exempt
def add_sns(request):
    form = SnsForm()
    sns_list = []
    if request.method == 'POST':
        sns_id = request.POST.get('sns_id','')
        url = request.POST.get('url','')
        title = request.POST.get('title','')
        types = request.POST.get('types','')
        duration = request.POST.get('duration','')

        return append_sns(sns_id, url, title, types, duration)
    else:
        form = SnsForm(
            initial={
                    'sns_id':1,
                    'url':1,
                    'title':"title",
                  }
              )

    objs = SnsModel.objects.all()
    sns_list = objs2dict_list(objs, g_sns_fields)
    #print pyUsage.get_cur_info(), 'sns_list= ', sns_list
    return render_to_response('add_sns.html', {'form': form, 'sns_list':sns_list})      

@csrf_exempt
def get_sns(request):
    objs = SnsModel.objects.all()
    sns_list = objs2dict_list(objs, g_sns_fields)
    sns_list = sns_list[:3]
    ###append comment
    #for i,v in enumerate(sns_list):
    for i,v in enumerate(sns_list):
        vid = v['sns_id']
        comments = CommentModel.objects.filter(sns_id=vid)
        if len(comments) > 0:
            #print pyUsage.get_cur_info(), 'g_comment_fields= ', g_comment_fields
            c_dict = objs2dict_list(comments, g_comment_fields)
            sns_list[i]['comment'] = c_dict

    return JsonResponse(
            {
                'status': 'success',
                'status_code':0,
                'cnt': len(sns_list),
                'sns_list':sns_list,
            })

@csrf_exempt
def del_sns(request):
    sns_id = request.POST.get('sns_id','')
    if len(sns_id) == 0:
        sns_id = request.GET.get('sns_id','')
    if len(sns_id) == 0:
        return HttpResponse('empty sns_id')
    
    e_list = SnsModel.objects.filter(sns_id = sns_id)
    if len(e_list) == 0:
        return HttpResponse('sns_id:%s not exists'%sns_id)

    assert(len(e_list) == 1)    
    e_list[0].delete()
    e_list = SnsModel.objects.filter(sns_id = sns_id)
    flag = True if len(e_list) == 0 else False
    return pack_json_resp(flag, 'del_sns error', -1)

@csrf_exempt
def add_comment(request):
    form = []
    if request.method == 'POST':
        sns_id = request.POST.get('sns_id','')
        comment = request.POST.get('comment', '')
        username = request.POST.get('username')
        if len(username) == 0:
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if len(comment) == 0:
            return pack_json_resp(False, 'comment is empty', -1)
        objs = SnsModel.objects.filter(sns_id=sns_id)
        if len(objs) != 1:
            return pack_json_resp(False, '[%s]sns id not exits'%sns_id, -1)

        c = CommentModel(
                sns_id = sns_id, 
                comment = comment, 
                username = username)
        ret = c.save()
        #print pyUsage.get_cur_info(), 'ret= ', ret
        return pack_json_resp(ret, 'add_comment error', -1)
    else:
        pass
    form = CommentForm(
            initial={
                'username':'18684016495',
                'sns_id':'14651978969257216923',
                'comment':'good film',
            }
    )
    return render_to_response('comment_sns.html', {'form':form})

@csrf_exempt
def update_sns(request):
    form = []
    if request.method == 'POST':
        sns_id = request.POST.get('sns_id','')
        if len(sns_id) == 0:
            sns_id = request.GET.get('sns_id','')
        if len(sns_id) == 0:
            return pack_json_resp(False, 'empty sns_id', -1)
        
        e_list = SnsModel.objects.filter(sns_id = sns_id)
        if len(e_list) == 0:
            return HttpResponse('sns_id:%s not exists'%sns_id)
        e_list = SnsModel.objects.filter(sns_id = sns_id)    
        #print pyUsage.get_cur_info(), 'len= ', len(e_list)
        assert(len(e_list) == 1)    

        e = e_list[0]
        ret = update_all_fields(e, request.POST)
        e_list = SnsModel.objects.filter(sns_id = sns_id)
        assert(len(e_list) == 1)

        return pack_json_resp(ret, 'update_sns error', -1)
    else:
        pass
    form = SnsForm(
        initial={
                #'sns_id':1,
                #'url':1,
                #'title':"title",
              }
          )
    return render_to_response('add_sns.html', {'form': form})
