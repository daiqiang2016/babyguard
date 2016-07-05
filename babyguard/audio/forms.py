#-*- coding: gb18030 -*-
from django import forms

class CommentForm(forms.Form):
    audio_id = forms.CharField()
    username = forms.CharField()
    comment = forms.CharField()

class AudioForm(forms.Form):
    audio_id = forms.CharField()
    url = forms.CharField()
    title = forms.CharField()
    type = forms.CharField()
    duration = forms.CharField()
