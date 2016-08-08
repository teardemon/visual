from django.conf.urls import patterns, url
from idc import views

urlpatterns = patterns('',
                       url(r'^$', views.CIDCTraff.as_view(), name='index'),
                       url(r'^type$', views.TypePercent, name='index'),
                       url(r'^img$', views.ImgTraff, name='index'),
                       url(r'^test$', views.CTest.as_view(), name='index'),
                       )
