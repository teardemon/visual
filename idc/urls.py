from django.conf.urls import patterns, url

from idc import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^type$', views.TypePercent, name='index'),
                       url(r'^img$', views.ImgTraff, name='index'),
                       )
