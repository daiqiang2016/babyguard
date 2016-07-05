#!/usr/bin/env python
#-*-coding:utf-8-*-

#author: jacky
# Time: 15-12-15
# Desc: 短信http接口的python代码调用示例
# https://www.yunpian.com/api/demo.html
# https访问，需要安装  openssl-devel库。apt-get install openssl-devel

import sys
#import httplib
import http.client as httplib
import urllib
import json
#服务地址
sms_host = "sms.yunpian.com"
voice_host = "voice.yunpian.com"
#端口号
port = 443
#版本号
version = "v2"
#查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
#智能匹配模版短信接口的URI
sms_send_uri = "/" + version + "/sms/single_send.json"
#模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_single_send.json"
#语音短信接口的URI
sms_voice_send_uri = "/" + version + "/voice/send.json"
#语音验证码
voiceCode = 1234
def get_user_info(apikey):
    """
    取账户信息
    """
    conn = httplib.HTTPSConnection(sms_host , port=port)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn.request('POST',user_get_uri,urllib.parse.urlencode( {'apikey' : apikey}))
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def api_send_sms(apikey, text, mobile):
    """
    通用接口发短信
    """
    params = urllib.parse.urlencode({'apikey': apikey, 'text': text, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.parse.urlencode({'apikey': apikey, 'tpl_id':tpl_id, 'tpl_value': urllib.parse.urlencode(tpl_value), 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def send_voice_sms(apikey, code, mobile):
    """
    通用接口发短信
    """
    params = urllib.parse.urlencode({'apikey': apikey, 'code': code, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(voice_host, port=port, timeout=30)
    conn.request("POST", sms_voice_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def send_sms(mobile, sms_code):
    apikey = "c7a3e11f8080fe32a031c956717af9d9"
    text = "您的验证码是"+str(sms_code)
    resp = api_send_sms(apikey,text,mobile)
    #f = open('resp.txt', 'wb')
    #f.write(resp)
    #f.close()
    resp = resp.decode('utf8')
    print ('[line:91]resp= ', resp)
    t = json.loads(resp)#, encoding='utf8')
    print ('t= ', t, 'sms_code= ', sms_code)
    ###这里返回整个串，携带错误信息，便于debug
    return t

if __name__ == '__main__':
    #修改为您的apikey.可在官网（http://www.yuanpian.com)登录后获取
    apikey = "c7a3e11f8080fe32a031c956717af9d9"
    #修改为您要发送的手机号码，多个号码用逗号隔开
    mobile = "18684016495"
    send_sms(mobile, '9527')
    sys.exit(0)

    #修改为您要发送的短信内容
    text = "您的验证码是9999"
    #查账户信息
    print(get_user_info(apikey))
    #调用智能匹配模版接口发短信
    print (api_send_sms(apikey,text,mobile))
    ##调用模板接口发短信
    #tpl_id = 1 #对应的模板内容为：您的验证码是#code#【#company#】
    #tpl_value = {'#code#':'1234','#company#':'云片网'}
    #tpl_id = 1338841 #对应的模板内容为：您的验证码是#code#【#company#】
    #tpl_value = {'#code#':'1234'}
    #print tpl_send_sms(apikey, tpl_id, tpl_value, mobile)
    ##调用模板接口发语音短信
    ##print send_voice_sms(apikey,voiceCode,mobile)
