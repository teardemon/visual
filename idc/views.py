# <coding:utf-8>
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.generic import View

import models


class CLineTraffic(View):
    def get(self, request, *args, **kwargs):
        object_result = models.notify.objects.all()
        return render(request, 'idc/pie.html', {'notifications': object_result})


def CImgTraffic(req):
    return render_to_response('idc/img_traffic.html')


def CTypePercent(req):
    return render_to_response('idc/bar_percent.html')


class CTest(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('idc/test.html')
