# <coding:utf-8>
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class notify(models.Model):
    content = models.CharField(max_length=200, help_text="显示在页面的通知信息")

    class Meta:
        db_table = "notify"

    def __str__(self):  # __unicode__ on Python 2
        return "adsl page notify"


class info(models.Model):
    ip = models.CharField(max_length=100, help_text="adsl ip")
    interface = models.CharField(max_length=100, help_text="网口信息")
    purpose = models.CharField(max_length=100, null=True, blank=True, help_text="用途，如网站")
    equrrdment = models.CharField(max_length=100, null=True, blank=True, help_text="设备类型，如ADSL，光纤")
    up_total = models.IntegerField(help_text="上行最大带宽")
    down_total = models.IntegerField(help_text="下行最大带宽")

    class Meta:
        db_table = "info"


'''
ull 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填
'''
