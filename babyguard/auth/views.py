# -*- coding: utf-8 -*-
import time
import datetime
import pyUsage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.shortcuts import render
#from babyguard.request_check import *
from urllib.parse import unquote
from django.shortcuts import render,render_to_response
from babyguard.helper import pack_json_resp, objs2dict_list, update_all_fields, JsonResponse
import json
import tencentyun

@csrf_exempt
def test(request):
    #print pyUsage.get_cur_info(), 'request=', str(request)
    #print pyUsage.get_cur_info(), 'request.GET=',request.GET
    #print pyUsage.get_cur_info(), 'request.POST=',request.POST
    return HttpResponse('test ok')

@csrf_exempt
def up_pic(request):
    from django.db import models
    t = dir(models.DateTimeField)
    t.sort()
    #print t
    demo = request.GET.get('demo', '')
    if len(demo) > 0:
        return render_to_response('up_pic2.html')
    else:
        return render_to_response('up_pic5.html')
        

@csrf_exempt
def auth(request):
    projectid = '10024906'
    bucket = 'babypic'
    userid = '0'
    secret_id = 'AKIDo4dnSRoYOV47rlzaKjPIg14QOzuTnP6K'
    secret_key = 'FaH8kRM7F7PFZgDzHtF9ge99fYGeIuSf'

    image = tencentyun.ImageV2(projectid,secret_id,secret_key)

    #print pyUsage.get_cur_info(), 'request=', str(request)
    #print pyUsage.get_cur_info(), 'request.POST= ', request.POST
    #print pyUsage.get_cur_info(), 'request.GET= ', request.GET
    #print pyUsage.get_cur_info(), 'request.body= ', request.body

    op_type = request.GET.get('type','')
    #fileid = request.GET.get('fileid','')
    topdir = request.GET.get('topdir','common')
    #filename = request.GET.get('filename', '')
    path = request.GET.get('path', '')
    filename = path.split('/')[-1]
    jsonp = request.GET.get('jsonp', '')
    date = datetime.datetime.now()
    second = date.strftime('%Y%m%d_%H%M%S')

    #print pyUsage.get_cur_info(), 'request.FILES= ', request.FILES
    #for i,k in enumerate(request.FILES['file']):
    #    #print i,k

    if 'upload' == op_type:
        #fileid = '/u/can/use/slash/sample'+str(int(time.time()))
        if len(filename) == 0:
            filename = 'sample'
        fileid = '/%s/%s/%s'%(topdir.encode('utf8'), second, filename.encode('utf8'))
        fileid = '/%s/%s/%s'%(topdir, second, filename)
        #fileid = fileid.encode('utf8')
        #print pyUsage.get_cur_info(), 'fileid= ', fileid
        expired = int(time.time()) + 999
        url = image.generate_res_url_v2(bucket,userid,fileid)
        auth = tencentyun.Auth(secret_id,secret_key)
        sign = auth.get_app_sign_v2(bucket, fileid, expired)
        #uploadFormret = {'status_code':0, 'url':url, 'sign':sign}
        ###
        url = url.replace('%2F','/')
        ret = {'url':url, 'sign':sign}
        #print pyUsage.get_cur_info(), 'ret=', ret
    #else:
    #    ret = {'status_code':0, 'ret':'ok', 'auth':'no'}
    elif 'download' == op_type:
        expired = int(time.time()) + 999
        auth = tencentyun.Auth(secret_id,secret_key)
        url = image.generate_res_url_v2(bucket,userid,fileid)
        sign = auth.get_app_sign_v2(bucket, fileid, expired)
        ret = {'sign':sign}
    else:
        if not fileid:
            ret = {'error':'params error'}
        else :
            if 'stat' == op_type:
                op_type = ''
            expired = 0
            auth = tencentyun.Auth(secret_id,secret_key)
            url = image.generate_res_url_v2(bucket,userid,fileid,op_type)
            sign = auth.get_app_sign_v2(bucket, fileid, expired)
            ret = {'url':url, 'sign':sign}

    #print pyUsage.get_cur_info(), 'op_type= ', op_type
    #print pyUsage.get_cur_info(), 'ret= ', ret
    if len(jsonp) > 0:
        #print pyUsage.get_cur_info(), 'ret= ', ret
        encodedjson = json.dumps(ret, indent = 4)
        #print pyUsage.get_cur_info(), 'encodedjson= ', encodedjson
        return HttpResponse('mycallback(%s)'%encodedjson)
    else:
        return JsonResponse(ret)
