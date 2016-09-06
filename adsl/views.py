# <coding:utf-8>
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.generic import View
from . import models

class CADSLTraffic(View):
    def get(self, request, *args, **kwargs):
        object_result = models.notify.objects.all()
        return render(request, 'adsl/bar.html', {'notifications': object_result})
