# -*- coding: utf-8 -*-

import logging
import json
import random
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

#from vr.account.models import BaseProfileModel, ProfileUserModel

###云通讯
#from CCPRestSDK import REST
###个推
#from vr.getuiSDK.igt_push import *
#from vr.getuiSDK.igetui.template import *
#from vr.getuiSDK.igetui.template.igt_base_template import *
#from vr.getuiSDK.igetui.template.igt_transmission_template import *
#from vr.getuiSDK.igetui.template.igt_link_template import *
#from vr.getuiSDK.igetui.template.igt_notification_template import *
#from vr.getuiSDK.igetui.template.igt_notypopload_template import *
#from vr.getuiSDK.igetui.template.igt_apn_template import *
#from vr.getuiSDK.igetui.igt_message import *
#from vr.getuiSDK.igetui.igt_target import *
#from vr.getuiSDK.igetui.template import *
#from vr.getuiSDK.BatchImpl import *
#from vr.getuiSDK.payload.APNPayload import *

import os
import hashlib
from hashlib import sha256,md5
from hmac import HMAC
import datetime
import pytz
import random
import re

os.environ['needDetails'] = 'true'
APPKEY = "8RlgiDyl2mAoCNFsmEoxj2"
APPID = "3JlGNEbMMZ7oNaBvvTFZi3"
MASTERSECRET = "U8NPJUhvgj9j8QdYuO4ZJ5"
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

# 透传模板动作内容
def TransmissionTemplateDemo():
    template = TransmissionTemplate()
    template.transmissionType = 1
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = '请填入透传内容'
    # iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
    # template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
#     template.setPushInfo("", 0, "", "com.gexin.ios.silence", "", "", "", "");

# APN简单推送
    alertMsg = SimpleAlertMsg()
    alertMsg.alertMsg = ""
    apn = APNPayload();
    apn.alertMsg = alertMsg
    apn.badge = 2
#     apn.sound = ""
    apn.addCustomMsg("payload", "payload")
#     apn.contentAvailable=1
#     apn.category="ACTIONABLE"
    template.setApnInfo(apn)

    # APN高级推送
#     apnpayload = APNPayload()
#     apnpayload.badge = 4
#     apnpayload.sound = "com.gexin.ios.silence"
#     apnpayload.addCustomMsg("payload", "payload")
# #     apnpayload.contentAvailable = 1
# #     apnpayload.category = "ACTIONABLE"
#     alertMsg = DictionaryAlertMsg()
#     alertMsg.body = 'body'
#     alertMsg.actionLocKey = 'actionLockey'
#     alertMsg.locKey = 'lockey'
#     alertMsg.locArgs=['locArgs']
#     alertMsg.launchImage = 'launchImage'
#     # IOS8.2以上版本支持
# #     alertMsg.title = 'Title'
# #     alertMsg.titleLocArgs = ['TitleLocArg']
# #     alertMsg.titleLocKey = 'TitleLocKey'
#     apnpayload.alertMsg=alertMsg
#     template.setApnInfo(apnpayload)
    
    
    return template

def pushMessageToSingle(CID):
    #http的接口
    # push = IGeTui(None, APPKEY, MASTERSECRET,False)
    #https的接口
    # push = IGeTui(None, APPKEY, MASTERSECRET,True)
    #根据HOST区分是https还是http
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板

#     template = NotificationTemplateDemo()
    # template = LinkTemplateDemo()
    template = TransmissionTemplateDemo()
    # template = NotyPopLoadTemplateDemo()
    
    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    # message.pushNetWorkType = 2

    target = Target()
    target.appId = APPID
    target.clientId = CID

    try:
        ret = push.pushMessageToSingle(message, target)
        #print ret
    except:# RequestException, e:
        requstId = e.getRequestId()
        ret = push.pushMessageToSingle(message, target, requstId)
        #print ret

def match_mobile(s):
    fmt = '1\d{10}'
    fmt += '|'
    fmt += '(\d{4}-|\d{3}-)?(\d{8}|\d{7})'
    pattern = re.compile(r'^%s$'%fmt)
    s = s.strip()
    match = pattern.match(s)
    if match:
        return True
    return False   

def encrypt_password(password, salt=None):
    """Hash password on the fly."""
    if salt is None:
        salt = os.urandom(8) # 64 bits.

    assert 8 == len(salt)
    assert isinstance(salt, str)

    if isinstance(password, unicode):
        password = password.encode('UTF-8')

    assert isinstance(password, str)

    result = password
    for i in xrange(10):
        result = HMAC(result, salt, sha256).digest()

    return salt + result

def md5(str):
    import hashlib
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

def validate_password(hashed, input_password):
    return hashed == encrypt_password(input_password, salt=hashed[:8])

def getNow():
    pytz.country_timezones('cn')
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz)

def clearTimeFlag(s):
    s = s.replace('-','')
    s = s.replace(':','')
    s = s.replace(' ','')
    return s

def getFormatTime2Second():
    dt = datetime.datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def getFormatTime():
    dt = datetime.datetime.now() 
    #dt.strftime('%Y-%m-%d %H:%M:%S %f') #2010-04-07 10:52:18 937000 
    #dt.strftime('%y-%m-%d %I:%M:%S %p') #10-04-07 10:52:18 AM  
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_random():
    ret = ""
    cnt = 4
    while cnt > 0:
        cnt = cnt - 1
        ret = ret + str(random.randint(0, 9))
    #logger.warning('%s', ret)
    return ret

def sendTemplateSMS(to, datas, tempId):
    #logger.warning("fuck to %s" % (to))
    accountSid= '8a48b5514a61a814014a6fe5eb81072f'
    accountToken = '15562e643d4843c1af2e16e62ac249b5'
    appId = '8a48b5514a61a814014a822bf9791409'
    serverIP = 'app.cloopen.com'
    serverPort = '8883'
    softVersion='2013-12-26'
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    result = rest.sendTemplateSMS(to,datas,tempId)
    for k,v in result.iteritems():
        if k=='templateSMS' :
            for k,s in v.iteritems():
                pass
                #logger.warning('%s:%s' % (k, s))
                #print '%s:%s' % (k, s)
        else:
            #print '%s:%s' % (k, v)
            pass

logger = logging.getLogger('django')

def JsonResponse(params):
    return HttpResponse(json.dumps(params, ensure_ascii = False, indent = 2))

def get_sig(post):
    params = []
    for key,value in post.iteritems():
        if key == 'sig':
            continue
        if key == 'headimg':
            continue
        params.append({'key': key, 'value': value})
    params = sorted(params, key = lambda x: x['key'])
    md5 = hashlib.md5()
    string = u'&'.join(u'%s=%s'%(param['key'], param['value']) for param in params)
    string += u'&' + AireCheckConstant.API_SECRET_KEY
    #logger.warning(u"Signature Failed. string = %s" %(string))
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()

class SigHTTPClient(Client):
    def _do_sig_req(self, url, data, method, *args, **kwargs):
        data.update(sig=get_sig(data))
        if method == 'GET':
            response = self.get(url, data, *args, **kwargs)
        elif method == 'POST':
            response = self.post(url, data, *args, **kwargs)
        decode = kwargs.get('decode', True)
        if decode:
            return json.loads(response.content)
        else:
            return response

    def do_post(self, url, data={}, *args, **kwargs):
        return self._do_sig_req(url, data, 'POST', *args, **kwargs)

    def do_get(self, url, data={}, *args, **kwargs):
        return self._do_sig_req(url, data, 'GET', *args, **kwargs)

def pack_json_resp(ret, err_msg, err_code, description = ''):
    resp = JsonResponse(
    {
        'status': 'success',
        'status_code':0
    })
    if ret != True:
        resp = JsonResponse(
            {
                'status': err_msg,
                'status_code':err_code,
                'description':description,
            }) 
    return resp

def objs2dict_list(objs, fields):
    d_list = []
    if objs is None:
        return d_list

    for obj in objs:
        d = {}
        #print (pyUsage.get_cur_info(), fields)
        for name in fields:
            d[name] = getattr(obj, name)
            if isinstance(d[name], datetime.datetime):
                t = d[name].strftime('%Y-%m-%d')
                d[name] = t
            else:    
                pass
                #print (pyUsage.get_cur_info(), type(d[name]) )
        d_list.append(d)
    return d_list

def update_all_fields(e, val_dict):
    for name in g_point_fields:
        v = val_dict.get(name,'')
        if len(v) != 0:
            setattr(e, name, v)
    ret = e.save()
    return ret

   
def get_md5(s):
    m2 = hashlib.md5()   
    m2.update(s.encode('utf8')) 
    print (m2.hexdigest())
    return m2.hexdigest()

def update_all_fields(e, field_list, val_dict):
    for name in field_list:
        v = val_dict.get(name,'')
        if len(v) != 0:
            setattr(e, name, v)
    ret = e.save()
    return ret
    
if __name__ == '__main__':
    hashed = encrypt_password('secret password')
    #print 'hashed= ', hashed
    assert validate_password(hashed, 'secret password')
    #print md5('secret password')
    
    #print match_mobile('18684016495')
    #print match_mobile('1868401649x5')
    #print match_mobile('021-86013238')
    #print match_mobile('86013238')

