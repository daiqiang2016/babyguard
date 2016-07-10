# -*- coding: utf-8 -*-
from redisco import models

class CommentModel(models.Model):
    sns_id = models.Attribute(required=True, unique = True)
    username = models.Attribute(required=False)
    comment = models.Attribute(required=False)
    created_at = models.DateTimeField(auto_now_add=False) 

class SnsModel(models.Model):
    sns_id = models.Attribute(required=True, unique = True)###id
    url = models.Attribute(required=False, default='')
    pics= models.Attribute(required=False, default='')
    title = models.Attribute(required=False, default='名称未知')
    types = models.Attribute(required=False, default='mp3')
    duration = models.Attribute(required=False, default='时长未知')
    created_at = models.DateTimeField(auto_now_add=False)
    
    #breakfast = models.Attribute(required=False, unique = False)###早餐
    #lunch = models.Attribute(required=False, unique = False)###午餐
    #dinner = models.Attribute(required=False, unique = False)###晚餐
    #created_at = models.DateTimeField(auto_now_add=False) 
    #
    #
    #name = models.Attribute(required=False, default='')###菜名
    #url = models.Attribute(required=False)    ###sns url
    #title = models.Attribute(required=False, default='影片标题')  ###标题 
    #pic = models.Attribute(required=False, default='图片暂无')###影片的大图
    #ower = models.Attribute(required=False,  default='上传者未知')  ###上传人员who upload the sns  
    #actors = models.Attribute(required=False,default='演员未知')###演员表film star
    #type = models.Attribute(required=False,  default='类型未知')  ###影片类型3D or 360 degree
    #length = models.Attribute(required=False,default='长度未知')###影片长度sns length == 2h 45min ?
    #size = models.Attribute(required=False,  default='大小未知')  ###影片大小sns size == 2G ? 
    #short_abs = models.Attribute(required=False,default='好电影')###简短摘要
    #abstract=models.Attribute(required=False,default='这是一个好电影')###影片摘要
    #country = models.Attribute(required=False,default='中国')###地区：日本
    #year = models.Attribute(required=False,  default='年代未知')###年代：2016年
    #score= models.FloatField(required=False, default=8.0)###分数：6.4
    #created_at = models.DateTimeField(auto_now_add=False) 
    #srt = models.Attribute(required=False)
    ####评论
    #comments = models.ListField(target_type=CommentModel)###text,time,username

