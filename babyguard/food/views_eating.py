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
#import tencentyun
from babyguard.food.forms import *
from babyguard.food.models import *
from babyguard.helper import JsonResponse
from babyguard.helper import pack_json_resp, objs2dict_list, update_all_fields
from babyguard.helper import get_md5

g_comment_fields=[e.name for e in CommentModel().fields]
g_eating_fields=[e.name for e in EatingModel().fields]
g_food_fields = [e.name for e in FoodModel().fields]
    
def append_eating(eating_id, day, pics, name, kind):
    print (pyUsage.get_cur_info(), locals())
    e = EatingModel(
          eating_id = eating_id,
          day = day,
          pics = pics,
          name = name, 
          kind = kind)
    ret = e.save()
    print (pyUsage.get_cur_info(), 'ret= ', ret)
    resp = pack_json_resp(ret, 'append_eating err', -1)
    return resp

@csrf_exempt
def reset_all_eating(request):
    e_list = EatingModel.objects.all()
    for e in e_list:
        e.delete()

    #f = '/data/babyguard/babyguard/babyguard/eating/all_eating.txt'
    f = os.path.split(os.path.realpath(__file__))[0] + '/all_eating.txt'
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
        eating_id = arr[0]
        title = arr[1]
        kind = arr[2]
        url = arr[3]
        day = ''
        ret = append_eating(eating_id, day, url, title, kind)       
        #print pyUsage.get_cur_info(), 'add ret= ', ret

    objs = EatingModel.objects.all()
    #print pyUsage.get_cur_info(), 'cnt= ', len(objs)
    eating_list = objs2dict_list(objs, g_eating_fields)
    #print pyUsage.get_cur_info(), 'cnt= ', len(eating_list)

    return JsonResponse(
            {
                'status': 'reset eating',
                'status_code':0,
                'cnt':len(eating_list),
                'eating_list':eating_list,
             })
    #print pyUsage.get_cur_info(), 'add ret= ', ret

@csrf_exempt
def add_eating(request):
    form = EatingForm()
    eating_list = []
    if request.method == 'POST':
        print (pyUsage.get_cur_info(), 'POST= ', request.POST)
        pics = request.POST.get('pics', '')
        print (pyUsage.get_cur_info(), 'url= ', pics)
        eating_id = request.POST.get('eating_id','')
        day = request.POST.get('day','')
        pics = request.POST.get('pics','')
        name = request.POST.get('name','')
        kind = request.POST.get('kind','')
        if len(day) == 0:
            return pack_json_resp(False, 'add_eating error! day is empty', -1)
        objs = EatingModel.objects.filter(day = day)
        if len(objs) > 0:
            return pack_json_resp(False, 'add_eating error! day already exists!', -1)

        if len(eating_id) == 0:
            eating_id = day

        return append_eating(eating_id, day, pics, name, kind)
    else:
        form = EatingForm(
            initial={
                    'eating_id':'2',
                    'day':'20160515',
                    'pics':'',
                    'name':'西红柿鸡蛋',
                    'kind':"3",
                  }
              )

    objs = EatingModel.objects.all()
    eating_list = objs2dict_list(objs, g_eating_fields)
    #print pyUsage.get_cur_info(), 'eating_list= ', eating_list
    #return render_to_response('add_eating.html', {'form': form, 'eating_list':eating_list})      
    return render_to_response('up_pic7.html', {'form': form, 'eating_list':eating_list})

@csrf_exempt
def get_eating(request):
    objs = EatingModel.objects.all()
    eating_list = objs2dict_list(objs, g_eating_fields)
    ###append comment
    for i,d in enumerate(eating_list):
        print (pyUsage.get_cur_info(), 'd= ', d)
        vid = d['eating_id']
        #comments = CommentModel.objects.filter(food_id=vid)
        #if len(comments) > 0:
        #    #print pyUsage.get_cur_info(), 'g_comment_fields= ', g_comment_fields
        #    c_dict = objs2dict_list(comments, g_comment_fields)
        #    eating_list[i]['comment'] = c_dict

    return JsonResponse(
            {
                'status': 'success',
                'status_code':0,
                'cnt': len(eating_list),
                'eating_list':eating_list,
            })

@csrf_exempt
def del_eating(request):
    eating_id = request.POST.get('eating_id','')
    if len(eating_id) == 0:
        eating_id = request.GET.get('eating_id','')
    if len(eating_id) == 0:
        return HttpResponse('empty eating_id')
    
    e_list = EatingModel.objects.filter(eating_id = eating_id)
    if len(e_list) == 0:
        return HttpResponse('eating_id:%s not exists'%eating_id)

    assert(len(e_list) == 1)    
    e_list[0].delete()
    e_list = EatingModel.objects.filter(eating_id = eating_id)
    flag = True if len(e_list) == 0 else False
    return pack_json_resp(flag, 'del_eating error', -1)

@csrf_exempt
def add_comment(request):
    form = []
    if request.method == 'POST':
        eating_id = request.POST.get('eating_id','')
        comment = request.POST.get('comment', '')
        username = request.POST.get('username')
        if len(username) == 0:
            return pack_json_resp(False, '[%s]not exists'%username, -1)
        if len(comment) == 0:
            return pack_json_resp(False, 'comment is empty', -1)
        objs = EatingModel.objects.filter(eating_id=eating_id)
        if len(objs) != 1:
            return pack_json_resp(False, '[%s]eating id not exits'%eating_id, -1)

        c = CommentModel(
                eating_id = eating_id, 
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
                'eating_id':'14651978969257216923',
                'comment':'good film',
            }
    )
    return render_to_response('comment_eating.html', {'form':form})

@csrf_exempt
def update_eating(request):
    form = []
    if request.method == 'POST':
        eating_id = request.POST.get('eating_id','')
        if len(eating_id) == 0:
            eating_id = request.GET.get('eating_id','')
        if len(eating_id) == 0:
            return pack_json_resp(False, 'empty eating_id', -1)
        
        e_list = EatingModel.objects.filter(eating_id = eating_id)
        if len(e_list) == 0:
            return HttpResponse('eating_id:%s not exists'%eating_id)
        e_list = EatingModel.objects.filter(eating_id = eating_id)    
        #print pyUsage.get_cur_info(), 'len= ', len(e_list)
        assert(len(e_list) == 1)    

        e = e_list[0]
        ret = update_all_fields(e, g_eating_fields, request.POST)
        e_list = EatingModel.objects.filter(eating_id = eating_id)
        assert(len(e_list) == 1)

        return pack_json_resp(ret, 'update_eating error', -1)
    else:
        pass
    form = EatingForm(
        initial={
                'pics':1,
                'name':1,
                'kind':"title",
              }
          )
    return render_to_response('add_eating.html', {'form': form})
