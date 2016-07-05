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
from babyguard.check.forms import *
from babyguard.check.models import *
from babyguard.helper import JsonResponse, pack_json_resp

g_check_fields = [e.name for e in CheckModel().fields]
g_comment_fields=[e.name for e in CommentModel().fields]
    
def append_check(check_id, username, day):
    e = CheckModel(
          check_id = check_id,
          username = username,
          day = day)
    ret = e.save()
    #print pyUsage.get_cur_info(), 'ret= ', ret
    resp = pack_json_resp(ret, 'append_check err', -1)
    return resp

def objs2dict_list(objs, fields):
    d_list = []
    for obj in objs:
        d = {}
        print (pyUsage.get_cur_info(), fields)
        for name in fields:
            d[name] = getattr(obj, name)
            if isinstance(d[name], datetime.datetime):
                t = d[name].strftime('%Y-%m-%d')
                d[name] = t
            else:    
                pass
                print (pyUsage.get_cur_info(), type(d[name]) )
        d_list.append(d)
    return d_list

def show_all_fields(e):
    #print pyUsage.get_cur_info(), 'e= ', dir(e)
    #print pyUsage.get_cur_info(), 'e= ', e.fields
    for name in g_check_fields:
        pass
        #print pyUsage.get_cur_info(), dir(name),type(name)
        #print pyUsage.get_cur_info(), 'name= ', name
        #print pyUsage.get_cur_info(), 'k,v=',name, getattr(name, '__str__')

def update_all_fields(e, val_dict):
    for name in g_check_fields:
        v = val_dict.get(name,'')
        if len(v) != 0:
            setattr(e, name, v)
    ret = e.save()
    return ret

@csrf_exempt
def reset_all_check(request):
    e_list = CheckModel.objects.all()
    for e in e_list:
        e.delete()

    #f = '/data/babyguard/babyguard/babyguard/check/all_check.txt'
    #f = os.path.split(os.path.realpath(__file__))[0] + '/all_check.txt'
    #t_list = pyIO.read_file_content(f, 'utf-8')
    #for t in t_list:
    #    #print pyUsage.get_cur_info(), 't= ', t
    #    t = t.strip()
    #    if t.find('http://') == -1:
    #        continue

    #    arr = t.split('\t')
    #    if len(arr) < 4:
    #        continue
    #    
    #    arr = t.split('\t')
    #    check_id = arr[0]
    #    title = arr[1]
    #    type = arr[2]
    #    url = arr[3]
    #    ret = append_check(check_id, url, title, type)       
    #    #print pyUsage.get_cur_info(), 'add ret= ', ret

    objs = CheckModel.objects.all()
    #print pyUsage.get_cur_info(), 'cnt= ', len(objs)
    check_list = objs2dict_list(objs, g_check_fields)
    #print pyUsage.get_cur_info(), 'cnt= ', len(check_list)

    return JsonResponse(
            {
                'status': 'reset check',
                'status_code':0,
                'cnt':len(check_list),
                'check_list':check_list,
             })
    #print pyUsage.get_cur_info(), 'add ret= ', ret

@csrf_exempt
def add_check(request):
    form = CheckForm()
    check_list = []
    if request.method == 'POST':
        check_id = request.POST.get('check_id','')
        username = request.POST.get('username','')
        day = request.POST.get('day','')

        return append_check(check_id, username, day)
    else:
        form = CheckForm(
            initial={
                    'check_id':1,
                    'url':1,
                    'title':"title",
                  }
              )

    objs = CheckModel.objects.all()
    check_list = objs2dict_list(objs, g_check_fields)
    #print pyUsage.get_cur_info(), 'check_list= ', check_list
    return render_to_response('add_check.html', {'form': form, 'check_list':check_list})      

@csrf_exempt
def get_check(request):
    objs = CheckModel.objects.all()
    check_list = objs2dict_list(objs, g_check_fields)
    ###append comment
    for i,v in enumerate(check_list):
        vid = v['check_id']
        comments = CommentModel.objects.filter(check_id=vid)
        if len(comments) > 0:
            #print pyUsage.get_cur_info(), 'g_comment_fields= ', g_comment_fields
            c_dict = objs2dict_list(comments, g_comment_fields)
            check_list[i]['comment'] = c_dict

    return JsonResponse(
            {
                'status': 'success',
                'status_code':0,
                'cnt': len(check_list),
                'check_list':check_list,
            })

@csrf_exempt
def del_check(request):
    check_id = request.POST.get('check_id','')
    if len(check_id) == 0:
        check_id = request.GET.get('check_id','')
    if len(check_id) == 0:
        return HttpResponse('empty check_id')
    
    e_list = CheckModel.objects.filter(check_id = check_id)
    if len(e_list) == 0:
        return HttpResponse('check_id:%s not exists'%check_id)

    assert(len(e_list) == 1)    
    e_list[0].delete()
    e_list = CheckModel.objects.filter(check_id = check_id)
    flag = True if len(e_list) == 0 else False
    return pack_json_resp(flag, 'del_check error', -1)

@csrf_exempt
def add_comment(request):
    form = []
    if request.method == 'POST':
        check_id = request.POST.get('check_id','')
        comment = request.POST.get('comment', '')
        username = request.POST.get('username')
        if len(username) == 0:
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if len(comment) == 0:
            return pack_json_resp(False, 'comment is empty', -1)
        objs = CheckModel.objects.filter(check_id=check_id)
        if len(objs) != 1:
            return pack_json_resp(False, '[%s]check id not exits'%check_id, -1)

        c = CommentModel(
                check_id = check_id, 
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
                'check_id':'14651978969257216923',
                'comment':'good film',
            }
    )
    return render_to_response('comment_check.html', {'form':form})

@csrf_exempt
def update_check(request):
    form = []
    if request.method == 'POST':
        check_id = request.POST.get('check_id','')
        if len(check_id) == 0:
            check_id = request.GET.get('check_id','')
        if len(check_id) == 0:
            return pack_json_resp(False, 'empty check_id', -1)
        
        e_list = CheckModel.objects.filter(check_id = check_id)
        if len(e_list) == 0:
            return HttpResponse('check_id:%s not exists'%check_id)
        e_list = CheckModel.objects.filter(check_id = check_id)    
        #print pyUsage.get_cur_info(), 'len= ', len(e_list)
        assert(len(e_list) == 1)    

        e = e_list[0]
        ret = update_all_fields(e, request.POST)
        e_list = CheckModel.objects.filter(check_id = check_id)
        assert(len(e_list) == 1)

        return pack_json_resp(ret, 'update_check error', -1)
    else:
        pass
    form = CheckForm(
        initial={
                #'check_id':1,
                #'url':1,
                #'title':"title",
              }
          )
    return render_to_response('add_check.html', {'form': form})
