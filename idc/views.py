# <coding:utf-8>
from django.shortcuts import render_to_response
from django.views.generic import View


class CLineTraffic(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('idc/pie.html')


class COnHookLineTraffic(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('idc/on_hook/pie.html')


def CImgTraffic(req):
    return render_to_response('idc/img_traffic.html')


def CTypePercent(req):
    return render_to_response('idc/bar_percent.html')


class CTest(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('idc/test.html')
