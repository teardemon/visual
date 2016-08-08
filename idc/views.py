# <coding:utf-8>
from django.shortcuts import render_to_response
from django.views.generic import View


class CIDCTraff(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('idc/pie.html')


def ImgTraff(req):
    return render_to_response('idc/imgtraff.html')


def TypePercent(req):
    return render_to_response('idc/barpercent.html')


class CTest(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('idc/test.html')
