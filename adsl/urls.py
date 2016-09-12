# <coding:utf-8>
from django.conf.urls import patterns, url
from adsl.views import *

urlpatterns = patterns('',
                       url(r'^$', CADSLTraffic.as_view(), {'on_hook': False}, name='adsl_index'),
                       url(r'^/input$', CADSLInput.as_view(), {'on_hook': False}, name='index'),
                       url(r'^/query$', CADSLQuery.as_view(), {'on_hook': False}, name='index'),
                       # url(r'^on_hook/line_traffic$', views.COnHookLineTraffic.as_view(), {'on-hook': True}, name='index'),
                       )

# url(r^/account/$', views.index, name=index)，它可以接收四个参数，
# 分别是两个必选参数：regex、view和两个可选参数：kwargs、name
