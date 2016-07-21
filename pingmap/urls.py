from django.conf.urls import patterns, url
#<coding:utf-8>
from pingmap import views

urlpatterns = patterns('',
	url(r'^$', views.index)
)
#	#url(r'^time/(.+)/$', views.index, name='test')
