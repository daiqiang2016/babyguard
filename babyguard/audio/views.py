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
from babyguard.audio.forms import *
from babyguard.audio.models import *
from babyguard.helper import JsonResponse, pack_json_resp,get_md5

g_audio_fields = [e.name for e in AudioModel().fields]
g_comment_fields=[e.name for e in CommentModel().fields]

def append_audio(audio_id, url, title, type, duration):
    e = AudioModel(
          audio_id = audio_id,
          url = url,
          title = title, 
          type = type,
          duration = duration)
    ret = e.save()
    print (pyUsage.get_cur_info(), 'ret= ', ret)
    resp = pack_json_resp(ret, 'append_audio err', -1)
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
    for name in g_audio_fields:
        pass
        #print pyUsage.get_cur_info(), dir(name),type(name)
        #print pyUsage.get_cur_info(), 'name= ', name
        #print pyUsage.get_cur_info(), 'k,v=',name, getattr(name, '__str__')

def update_all_fields(e, val_dict):
    for name in g_audio_fields:
        v = val_dict.get(name,'')
        if len(v) != 0:
            setattr(e, name, v)
    ret = e.save()
    return ret

@csrf_exempt
def reset_all_audio(request):
    e_list = AudioModel.objects.all()
    for e in e_list:
        e.delete()

    #f = '/data/babyguard/babyguard/babyguard/audio/all_audio.txt'
    f = os.path.split(os.path.realpath(__file__))[0] + '/all_audio.txt'
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
        audio_id = get_md5(arr[0])
        url = arr[0]
        title = arr[1]
        type = arr[2]
        duration = arr[3]
        ret = append_audio(audio_id, url, title, type, duration)       
        print (pyUsage.get_cur_info(), 'add ret= ', ret)

    objs = AudioModel.objects.all()
    #print pyUsage.get_cur_info(), 'cnt= ', len(objs)
    audio_list = objs2dict_list(objs, g_audio_fields)
    #print pyUsage.get_cur_info(), 'cnt= ', len(audio_list)

    return JsonResponse(
            {
                'status': 'reset audio',
                'status_code':0,
                'cnt':len(audio_list),
                'audio_list':audio_list,
             })
    #print pyUsage.get_cur_info(), 'add ret= ', ret

@csrf_exempt
def add_audio(request):
    form = AudioForm()
    audio_list = []
    if request.method == 'POST':
        audio_id = request.POST.get('audio_id','')
        url = request.POST.get('url','')
        title = request.POST.get('title','')
        type = request.POST.get('type','')
        duration = request.POST.get('duration','')

        return append_audio(audio_id, url, title, type, duration)
    else:
        form = AudioForm(
            initial={
                    'audio_id':1,
                    'url':1,
                    'title':"title",
                  }
              )

    objs = AudioModel.objects.all()
    audio_list = objs2dict_list(objs, g_audio_fields)
    #print pyUsage.get_cur_info(), 'audio_list= ', audio_list
    return render_to_response('add_audio.html', {'form': form, 'audio_list':audio_list})      

@csrf_exempt
def get_audio(request):
    objs = AudioModel.objects.all()
    audio_list = objs2dict_list(objs, g_audio_fields)
    audio_list = audio_list[:3]
    ###append comment
    #for i,v in enumerate(audio_list):
    for i,v in enumerate(audio_list):
        vid = v['audio_id']
        comments = CommentModel.objects.filter(audio_id=vid)
        if len(comments) > 0:
            #print pyUsage.get_cur_info(), 'g_comment_fields= ', g_comment_fields
            c_dict = objs2dict_list(comments, g_comment_fields)
            audio_list[i]['comment'] = c_dict

    return JsonResponse(
            {
                'status': 'success',
                'status_code':0,
                'cnt': len(audio_list),
                'audio_list':audio_list,
            })

@csrf_exempt
def del_audio(request):
    audio_id = request.POST.get('audio_id','')
    if len(audio_id) == 0:
        audio_id = request.GET.get('audio_id','')
    if len(audio_id) == 0:
        return HttpResponse('empty audio_id')
    
    e_list = AudioModel.objects.filter(audio_id = audio_id)
    if len(e_list) == 0:
        return HttpResponse('audio_id:%s not exists'%audio_id)

    assert(len(e_list) == 1)    
    e_list[0].delete()
    e_list = AudioModel.objects.filter(audio_id = audio_id)
    flag = True if len(e_list) == 0 else False
    return pack_json_resp(flag, 'del_audio error', -1)

@csrf_exempt
def add_comment(request):
    form = []
    if request.method == 'POST':
        audio_id = request.POST.get('audio_id','')
        comment = request.POST.get('comment', '')
        username = request.POST.get('username')
        if len(username) == 0:
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if len(comment) == 0:
            return pack_json_resp(False, 'comment is empty', -1)
        objs = AudioModel.objects.filter(audio_id=audio_id)
        if len(objs) != 1:
            return pack_json_resp(False, '[%s]audio id not exits'%audio_id, -1)

        c = CommentModel(
                audio_id = audio_id, 
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
                'audio_id':'14651978969257216923',
                'comment':'good film',
            }
    )
    return render_to_response('comment_audio.html', {'form':form})

@csrf_exempt
def update_audio(request):
    form = []
    if request.method == 'POST':
        audio_id = request.POST.get('audio_id','')
        if len(audio_id) == 0:
            audio_id = request.GET.get('audio_id','')
        if len(audio_id) == 0:
            return pack_json_resp(False, 'empty audio_id', -1)
        
        e_list = AudioModel.objects.filter(audio_id = audio_id)
        if len(e_list) == 0:
            return HttpResponse('audio_id:%s not exists'%audio_id)
        e_list = AudioModel.objects.filter(audio_id = audio_id)    
        #print pyUsage.get_cur_info(), 'len= ', len(e_list)
        assert(len(e_list) == 1)    

        e = e_list[0]
        ret = update_all_fields(e, request.POST)
        e_list = AudioModel.objects.filter(audio_id = audio_id)
        assert(len(e_list) == 1)

        return pack_json_resp(ret, 'update_audio error', -1)
    else:
        pass
    form = AudioForm(
        initial={
                #'audio_id':1,
                #'url':1,
                #'title':"title",
              }
          )
    return render_to_response('add_audio.html', {'form': form})
