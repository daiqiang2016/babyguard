#-*- coding: gb18030 -*-
from django import forms

class CommentForm(forms.Form):
    check_id = forms.CharField()
    username = forms.CharField()
    comment = forms.CharField()

class CheckForm(forms.Form):
    check_id = forms.CharField()
    username = forms.CharField()
    day = forms.CharField()

    #title = forms.CharField()
    #ower= forms.CharField()
    #actors = forms.CharField()
    #type = forms.CharField()
    #length = forms.CharField()
    #size = forms.CharField()
    #abstract = forms.CharField()
    #country = forms.CharField()
    #year = forms.CharField()
    #score = forms.FloatField()
