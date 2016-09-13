# <coding:utf-8>
# from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.views.generic import View
import json
import os
from conf import *
from opspro.public import keycache
from opspro.public.define import *


# Create your views here.
class CInterface(View):
    def __init__(self, str_key='public'):
        self.m_list_html = ['bar.html']
        self.m_json_respond = {}
        self.m_object_key_store = self.init_db(str_key)

    def is_db(self, str_key):
        str_name_db = self.get_name_db(str_key)
        str_path_db = self.get_path_db(str_name_db)
        if os.path.isfile(str_path_db):
            return 1
        return 0

    def init_db(self, str_key):
        str_name_db = self.get_name_db(str_key)
        str_path_db = self.get_path_db(str_name_db)
        return keycache.CKeyStore(str_path_db)

    def get_name_db(self, str_key):
        str_name_db = '{0}.{1}'.format(str_key, 'db')
        return str_name_db

    def get_show_html(self, request):
        str_chart = request.GET.get('chart')
        str_html = '{0}.{1}'.format(str_chart, 'html')
        if str_html in self.m_list_html:
            return 'custom/{0}'.format(str_html)
        self.m_json_respond = self.get_respond({}, 0, 'type {0} is not exist'.format(str_html))
        return ''

    def get_path_db(self, str_name_db):
        str_path_db = STR_PATH_KEY_VALUE.format(str_name_db)
        return str_path_db

    def get_respond(self, dict_result={}, bool_success=1, str_tip=''):  # 一些语言的true必须大写开头，有的又不等于１．所以通用１
        if not isinstance(dict_result, dict):
            bool_success = 0
            str_tip = 'get_respond的第一个参数必须是字典'
            dict_result = {}
        dict_respond = {
            'result': dict_result,
            'success': bool_success,
            'tip': str_tip
        }
        json_respond = json.dumps(dict_respond)
        return json_respond

    def transfer_format(self, *args, **kwargs):
        if not args:
            self.m_json_respond = self.get_respond({}, 0, 'expect args')
        try:
            dict_input = eval(args[0])
        except:
            self.m_json_respond = self.get_respond({}, 0, 'expect json as input')
            return {}
        else:
            if not isinstance(dict_input, dict):
                self.m_json_respond = self.respond({}, 0, 'expect json as input')
            return dict_input


class CInput(CInterface):
    '''
    用于接受数据输入，数据作为键值对缓存被保存起来
    '''

    def __init__(self):
        super(CInput, self).__init__()
        self.m_dict_request = {
            'key': '',
            'data': json.dumps({}),
            'commit': '',
        }

    def deal_input(self):
        dict_data = self.m_dict_request['data']
        dict_input = self.transfer_format(dict_data)
        if not dict_input:
            return
        str_key = self.m_dict_request['key']
        str_date = self.m_dict_request['date']
        if not str_date:
            str_date = GetTime()
        self.m_object_key_store = self.init_db(str_key)
        dict_cache = {'lately': {
            'data': dict_data,
            'key': self.m_dict_request['key'],
            'date': str_date
        }}
        self.m_object_key_store.store(dict_cache)
        self.m_json_respond = self.get_respond()

    def is_enable_format(self, request):
        if not request.GET.get('key') or not request.GET.get('data'):
            self.m_json_respond = self.get_respond({}, 1, 'need two param at least: key and data')
            return 0
        return 1

    def get(self, request):
        if not self.is_enable_format(request):
            return HttpResponse(self.m_json_respond)
        self.m_dict_request = {
            'key': request.GET.get('key'),
            'data': request.GET.get('data'),
            'date': request.GET.get('date')
        }
        self.deal_input()
        # live == 1 对传入的数据进行可视化的效果直播，同时依然进行数据的存储
        if not request.GET.get('live') == '1':
            return HttpResponse(self.m_json_respond)
        str_html = self.get_show_html(request)
        if str_html:
            return render_to_response(str_html)
        else:
            return HttpResponse(self.m_json_respond)


class COutput(CInterface):
    '''
    读取新数据并输出
    '''

    def __init__(self):
        super(COutput, self).__init__()
        self.m_dict_request = {
            'key': '',
        }

    def deal_ouput(self, str_key):
        if not self.is_db(str_key):
            return
        self.m_object_key_store = self.init_db(str_key)
        if self.m_object_key_store.has_key('lately'):
            str_dict_output = self.m_object_key_store.key('lately')
            dict_output = eval(str_dict_output)
            dict_output = {
                'data': eval(dict_output['data']),  # 可能是编码的原因，eval对嵌套的内层字典没自动转换数据结构
                'key': dict_output['key'],
                'date': dict_output['date']
            }
            self.m_json_respond = self.get_respond(dict_output, 1, '')
        else:
            self.m_json_respond = self.get_respond({}, 1, 'data is null')

    def get_timeout(self, request):
        str_timeout = request.GET.get('timeout')
        if not str_timeout:
            return 0
        int_timeout = int(str_timeout)
        int_timeout = int_timeout * 1000  # setTimeout是以毫秒为单位的，转为ｓ
        return int_timeout

    def get(self, request):
        str_key = request.GET.get('key')
        if not str_key:
            self.m_json_respond = self.get_respond({}, 1, 'key is need')
        if not self.is_db(str_key):
            self.m_json_respond = self.get_respond({}, 0, 'key:{0} is not exist'.format(str_key))
            return HttpResponse(self.m_json_respond)
        self.deal_ouput(str_key)
        if not request.GET.get('chart'):
            return HttpResponse(self.m_json_respond)
        str_html = self.get_show_html(request)
        if not str_html:
            return HttpResponse(self.m_json_respond)
        int_timeout = self.get_timeout(request)
        print '------------------------', int_timeout
        return render_to_response(str_html, {'int_setTimeout': int_timeout})
