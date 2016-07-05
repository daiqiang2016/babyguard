# -*- coding: utf-8 -*-
from redisco import models

class CommentModel(models.Model):
    food_id = models.Attribute(required=True, unique = False)
    username = models.Attribute(required=True)
    comment = models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True) 

class EatingModel(models.Model):
    eating_id = models.Attribute(required=True, unique = True)###id
    day = models.Attribute(required=False, default='')
    pics = models.Attribute(required=False, default='')###图片
    name = models.Attribute(required=False, default='')###名字
    kind = models.Attribute(required=False, default='')###类型（点心、正餐）
    created_at = models.DateTimeField(auto_now_add=True) 
    
class FoodModel(models.Model):
    food_id = models.Attribute(required=True, unique = True)###id
    day = models.Attribute(required=False, default = '',)###
    breakfast = models.Attribute(required=False, default='')###早餐
    lunch = models.Attribute(required=False, default='')###午餐
    dinner = models.Attribute(required=False, default='')###晚餐
    created_at = models.DateTimeField(auto_now_add=True) 
    
