# <coding:utf-8>
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class notify(models.Model):
    content = models.CharField(max_length=200, help_text="显示在页面的通知信息")

    def __str__(self):  # __unicode__ on Python 2
        return "adsl page notify"


class info(models.Model):
    ip = models.CharField(max_length=100, help_text="adsl ip")
    interface = models.CharField(max_length=100, help_text="网口信息")
    up_total = models.IntegerField(help_text="上行最大带宽")
    download_total = models.IntegerField(help_text="下行最大带宽")
