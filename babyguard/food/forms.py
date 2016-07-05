#-*- coding: gb18030 -*-
from django import forms

class CommentForm(forms.Form):
    food_id = forms.CharField()
    username = forms.CharField()
    comment = forms.CharField()

class EatingForm(forms.Form):
    eating_id = forms.CharField()
    day = forms.CharField()
    pics = forms.CharField()
    name = forms.CharField()
    kind = forms.CharField()
    
class FoodForm(forms.Form):
    food_id = forms.CharField()
    day = forms.CharField()
    breakfast = forms.CharField()
    lunch = forms.CharField()
    dinner = forms.CharField()
