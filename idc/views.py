# <coding:utf-8>
from django.shortcuts import render_to_response
from django.http import HttpResponse  # return HttpResponse(dData)

# 完全使用ajax获得数据，不传递参数
def index(req):
    # jData = apiquery.ApiQuery()
    return render_to_response('idc/pie.html')

def ImgTraff(req):
    return render_to_response('idc/imgtraff.html')


def TypePercent(req):
    return render_to_response('idc/barpercent.html')
