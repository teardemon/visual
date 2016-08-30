# <coding:utf-8>
from django.conf.urls import patterns, url
from custom import views

##http://127.0.0.1/zabbix/chart?ip=116.211.88.27

urlpatterns = patterns('',
                       url(r'^input/$', views.CInput.as_view(), name='index'),
                       url(r'^output/$', views.COutput.as_view(), name='index'),
                       )

# url(r^/account/$', views.index, name=index)，它可以接收四个参数，
# 分别是两个必选参数：regex、view和两个可选参数：kwargs、name
