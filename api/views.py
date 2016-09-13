# -*- coding: utf-8 -*-
# from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.shortcuts import HttpResponse
from opspro.public.define import *


class CAlert(View):
    def get(self, request, *args, **kwargs):
        if not request.method == 'GET':  # and request.is_ajax():
            return HttpResponse()
        unicode_content = request.GET.get('content')
        unicode_number = request.GET.get('number')
        if not unicode_content or not unicode_number:
            return HttpResponse('必须参数：报警内容content,报警火星号number')
        ExecManagerFunc('alert', 'Alert', unicode_content, unicode_number)
        return HttpResponse()


class CLog(View):
    def get(self, request, *args, **kwargs):
        if not request.method == 'GET':  # and request.is_ajax():
            return HttpResponse()
        unicode_content = request.GET.get('content')
        unicode_path = request.GET.get('path')
        if not unicode_content or not unicode_path:
            return HttpResponse('必须参数：报警内容content,报警火星号number')
        ExecManagerFunc('log', 'Log', unicode_content, unicode_path)
        return HttpResponse()
