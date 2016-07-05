# -*- coding: utf-8 -*-
from redisco import models

class CommentModel(models.Model):
    audio_id = models.Attribute(required=True, unique = False)
    username = models.Attribute(required=True)
    comment = models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True) 

class AudioModel(models.Model):
    audio_id = models.Attribute(required=True, unique = True)###id
    url = models.Attribute(required=True, default='')
    title = models.Attribute(required=True, default='名称未知')
    type = models.Attribute(required=True, default='mp3')
    duration = models.Attribute(required=True, default='时长未知')
    created_at = models.DateTimeField(auto_now_add=True)
    
    #breakfast = models.Attribute(required=True, unique = True)###早餐
    #lunch = models.Attribute(required=True, unique = True)###午餐
    #dinner = models.Attribute(required=True, unique = True)###晚餐
    #created_at = models.DateTimeField(auto_now_add=True) 
    #
    #
    #name = models.Attribute(required=False, default='')###菜名
    #url = models.Attribute(required=True)    ###audio url
    #title = models.Attribute(required=False, default='影片标题')  ###标题 
    #pic = models.Attribute(required=False, default='图片暂无')###影片的大图
    #ower = models.Attribute(required=False,  default='上传者未知')  ###上传人员who upload the audio  
    #actors = models.Attribute(required=False,default='演员未知')###演员表film star
    #type = models.Attribute(required=False,  default='类型未知')  ###影片类型3D or 360 degree
    #length = models.Attribute(required=False,default='长度未知')###影片长度audio length == 2h 45min ?
    #size = models.Attribute(required=False,  default='大小未知')  ###影片大小audio size == 2G ? 
    #short_abs = models.Attribute(required=False,default='好电影')###简短摘要
    #abstract=models.Attribute(required=False,default='这是一个好电影')###影片摘要
    #country = models.Attribute(required=False,default='中国')###地区：日本
    #year = models.Attribute(required=False,  default='年代未知')###年代：2016年
    #score= models.FloatField(required=False, default=8.0)###分数：6.4
    #created_at = models.DateTimeField(auto_now_add=True) 
    #srt = models.Attribute(required=False)
    ####评论
    #comments = models.ListField(target_type=CommentModel)###text,time,username

