# -*- coding: utf-8 -*-
import sys
sys.path.extend([
                '/data/aircheck/aircheck/account/activity/',
                '/data/aircheck/aircheck/account/account/',
])

from redisco import models

class HistoryModel(models.Model):
    username = models.Attribute(required=True)
    video_id = models.Attribute(required=True, unique = False)
    created_at = models.DateTimeField(auto_now_add=True) 

class CollectModel(models.Model):
    username = models.Attribute(required=True)
    video_id = models.Attribute(required=True, unique = False)
    created_at = models.DateTimeField(auto_now_add=True) 

class ProfileModel(models.Model):
    username = models.Attribute(required=True, unique = True)###id
    password = models.Attribute(required=False)    ###
    sms_code = models.Attribute(required=False)  
    device = models.Attribute(required=False)###眼镜设备
    created_at = models.DateTimeField(auto_now_add=True) 

