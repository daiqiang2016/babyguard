#-*- coding: utf-8 -*-
from django import forms

class HistoryForm(forms.Form):
    video_id = forms.CharField()
    username = forms.CharField()

class CollectForm(forms.Form):
    video_id = forms.CharField()
    username = forms.CharField()

class ResetPasswordForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(required=False)
    sms_code = forms.CharField()

class ModifyPasswordForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    new_password = forms.CharField()

class RegisterAppUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    sms_code = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class ProfileForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class DeviceForm(forms.Form):
    username = forms.CharField()
    device = forms.CharField()
