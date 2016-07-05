#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
import babyguard.food.views_food as views_food
import babyguard.food.views_eating as views_eating

urlpatterns = [
    url('add_food$', views_food.add_food, name='add_food'),
    url('get_food$', views_food.get_food, name='get_food'),
    url('del_food$', views_food.del_food, name='del_food'),
    url('update_food$', views_food.update_food, name='update_food'),
    url('reset_all_food$', views_food.reset_all_food, name='reset_all_food'),
    url('add_comment$', views_food.add_comment, name='add_comment'),

    url('add_eating$', views_eating.add_eating, name='add_eating'),
    url('get_eating$', views_eating.get_eating, name='get_eating'),
    url('del_eating$', views_eating.del_eating, name='del_eating'),
    url('update_eating$', views_eating.update_eating, name='update_eating'),
    url('reset_all_eating$', views_eating.reset_all_eating, name='reset_all_eating'),
]
