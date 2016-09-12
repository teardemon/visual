# <coding:utf-8>
from django.contrib import admin

from .models import *


class NotifyAdmin(admin.ModelAdmin):
    modelField = notify._meta.fields
    list_display = [i.name for i in modelField]


admin.site.register(notify, NotifyAdmin)


class InfoAdmin(admin.ModelAdmin):
    modelField = info._meta.fields
    list_display = [i.name for i in modelField]


admin.site.register(info, InfoAdmin)
