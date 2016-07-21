from django.conf.urls import patterns, url

from adsl import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^time/(.+)/$', views.index, name='test')
)
