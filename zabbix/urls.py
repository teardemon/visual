# <coding:utf-8>
from django.conf.urls import patterns, url
from zabbix import views

##http://127.0.0.1/zabbix/chart?ip=116.211.88.27

urlpatterns = patterns('',
                       url(r'^chart$', views.CChart.as_view(), {'on_hook': False}, name='index'),
                       )

# url(r^/account/$', views.index, name=index)，它可以接收四个参数，
# 分别是两个必选参数：regex、view和两个可选参数：kwargs、name
