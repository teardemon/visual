# <coding:utf-8>
from django.conf.urls import patterns, url
from idc import views

urlpatterns = patterns('',
                       url(r'^$', views.CLineTraffic.as_view(), {'on_hook': False}, name='index'),
                       url(r'^line_traffic$', views.CLineTraffic.as_view(), {'on_hook': False}, name='index'),
                       url(r'^on_hook/line_traffic$', views.COnHookLineTraffic.as_view(), {'on-hook': True}, name='index'),

                       url(r'^type$', views.CTypePercent, name='index'),
                       url(r'^img$', views.CImgTraffic, name='index'),
                       url(r'^test$', views.CTest.as_view(), name='index'),
                       )

# url(r^/account/$', views.index, name=index)，它可以接收四个参数，
# 分别是两个必选参数：regex、view和两个可选参数：kwargs、name
