"""babyguard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('babyguard.account.urls')),
    #url(r'^ask/', include('babyguard.ask.urls')),
    url(r'^audio/', include('babyguard.audio.urls')),
    url(r'^check/', include('babyguard.check.urls')),
    url(r'^chart/', include('babyguard.chart.urls')),
    #url(r'^course/', include('babyguard.course.urls')),
    url(r'^food/', include('babyguard.food.urls')),
    url(r'^auth/', include('babyguard.auth.urls')),
    #url(r'^video/', include('babyguard.video.urls')),
    url(r'^sns/', include('babyguard.sns.urls')),
    url(r'^lab/', include('babyguard.lab.urls')),
]
