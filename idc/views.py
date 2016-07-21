# <coding:utf-8>
from django.shortcuts import render_to_response

from manager.rrdfile import *


def index(req, period='30day'):
    json_data = get_all_rrd_data(period)
    return render_to_response('idc.html', {'json_data': json_data, 'period': period})
