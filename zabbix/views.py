# <coding:utf-8>
from django.shortcuts import HttpResponse
from django.views.generic import View
import re
import json
import ast
from conf import *
from opspro.public import spider
from opspro.public import keycache
from opspro.public.define import *


# 用途：传一个ip，返回两组html标签。分别为该ip的一天和七天流量记录
# 流程：查询ip是交换机ip还是服务器ip

# demo host:http://127.0.0.1/zabbix/chart/113.106.204.9
# demo switch:http://127.0.0.1/zabbix/chart/113.106.204.126


class CChart(View, spider.CSpider):
    m_zabbix_chart_full = 'http://10.32.18.176:8088/zapi/graph/?id=123&ip={0}&type={1}'  # {0}为ip，type为’host‘或者‘switch’
    m_zabbix_chart_traffic = 'http://10.32.64.64/zabbix/chart2.php?graphid={0}&period={1}&updateProfile=1&profileIdx=web.screens&width=900'
    m_object_key_store = keycache.CKeyStore(STR_PATH_IDC_KEY_VALUE)

    # m_dict_map = DICT_SWITCH_MAP  # 定位一个graph id即定位一个网口。需要ＩＰ和网口名称，该字典将传入的线路名称转为网口名称。
    # 用get_switch_map而不用m_dict_map是考虑配置文件ip_to_interface.yaml需要自动更新

    def __init__(self):
        # 为了方便获得数据，使用一个字典来维持在该类中需要用到的参数。这样数据传递不会乱，而且数据结构直观
        self.m_dict_ret = {
            'traffic': {
                '1day': self.m_zabbix_chart_traffic,
                '7day': self.m_zabbix_chart_traffic,
                'graphid': '',  # 对应zabbix的graph id
            },
            'type': '',  # host or switch
            'ip': '',
            'line': '',  # 线路，不同线路能使用一个交换机ip，所以单靠交换机ip无法区分线路
            'info': '',  # zabbix查询得到的信息
        }

    # 判断一个ip返回的信息是交换机所有的
    def get_info(self):
        '''
        :return: 返回zabbix接口中关于一个ip的所有信息
        '''
        str_ip = self.m_dict_ret['ip']
        if str_ip in get_switch_map():
            str_api_url_zabbix = self.m_zabbix_chart_full.format(str_ip, 'switch')
            self.m_dict_ret['type'] = 'switch'
            self.m_dict_ret['info'] = str_api_url_zabbix
        else:
            str_api_url_zabbix = self.m_zabbix_chart_full.format(str_ip, 'host')
            self.m_dict_ret['type'] = 'host'
            self.m_dict_ret['info'] = str_api_url_zabbix
        json_info = self.ReadJson(str_api_url_zabbix)
        return json_info

    def get_interface_key(self):
        if self.m_dict_ret['interface']:
            return 'Traffic on interface {0}'.format(self.m_dict_ret['interface'])
        else:
            return 'Traffic on interface eth0'

    def get_server_chart_url(self, list_ret):
        str_interface_key = self.get_interface_key()
        for dict_item in list_ret:
            str_url = dict_item.get(str_interface_key, None)
            if str_url:
                return str_url
        str_msg_alert = '{0}通过接口查询关键字"{1}"没能在zabbix接口中获得关于zabbix流量图的url信息.可能原因:\n1.这个IP是缓存配置ip_to_interface.yaml中不存在的新交换机IP,通过删除缓存解决。\n2.这是一个配置不标准的服务器'.format(
            self.m_dict_ret['ip'],
            'Traffic on interface eth0')
        ExecManagerFunc('log', 'Log', str_msg_alert, 'error/level2')
        ExecManagerFunc('alert', 'Alert', str_msg_alert, [YouZeShun,QiangYao,ChenWuJie])
        return ''

    def get_switch_chart_url(self, list_ret):
        str_ip = self.m_dict_ret['ip']
        str_line = self.m_dict_ret['line']
        str_interface = get_interface(str_ip, str_line)
        for dict_interface_url in list_ret:
            for str_full_interface, str_url in dict_interface_url.iteritems():
                if str_interface in str_full_interface:
                    return str_url

    def get_chart_url(self, json_info):
        '''
        :param json_info:
        :return: 类型#http://10.32.64.64/zabbix/chart2.php?graphid=50832&period=3600&updateProfile=1&profileIdx=web.screens&width=900
        '''
        if not json_info:
            return ''
        if not isinstance(json_info, dict):
            return ''
        if not json_info.has_key('result'):
            return ''
        ret = json_info['result']
        if isinstance(ret, dict):
            # 字典说明错了
            return ''
        if self.m_dict_ret['type'] == 'host':
            str_traffic_url_demo = self.get_server_chart_url(ret)
        elif self.m_dict_ret['type'] == 'switch':
            str_traffic_url_demo = self.get_switch_chart_url(ret)
        else:
            str_traffic_url_demo = ''
        return str_traffic_url_demo

    def get_graph_id(self, str_traffic_url_demo):
        '''
        :param str_traffic_url_demo: 例如# http://10.32.64.64/zabbix/chart2.php?graphid=50832&period=3600&updateProfile=1&profileIdx=web.screens&width=600
        :return: None。仅仅从demo url中提取出 graph id 保存起来
        '''
        if not str_traffic_url_demo:
            str_error_msg = '不能获得IP为 {0} 的zabbix的graphid,因为没匹配成功。被匹配的对象: {1} 请检查该ip是否能从接口获得数据 {2}'.format(
                self.m_dict_ret['ip'], str_traffic_url_demo, self.m_dict_ret['info'])
            ExecManagerFunc('log', 'Log', str_error_msg, 'error/level2')
            ExecManagerFunc('alert', 'Alert', str_error_msg, [YouZeShun,ChenWuJie,QiangYao])
            return ''
        object_ret = re.search('(?<=graphid=)\d+', str_traffic_url_demo)
        if object_ret:
            self.m_dict_ret['traffic']['graphid'] = object_ret.group(0)
        if not self.m_dict_ret['traffic']['graphid']:
            str_error_msg = '不能获得IP为 {0} 的zabbix的graphid,因为没匹配成功。被匹配的对象: {1} 请检查该ip是否能从接口获得数据 {2}：'.format(
                self.m_dict_ret['ip'], str_traffic_url_demo, self.m_dict_ret['info'])
            ExecManagerFunc('log', 'Log', str_error_msg, 'error/level2')
            ExecManagerFunc('alert', 'Alert', str_error_msg, [YouZeShun,QiangYao,ChenWuJie])

    def assemble(self):
        str_graph_id = self.m_dict_ret['traffic']['graphid']
        if not str_graph_id:
            return ''
        self.m_dict_ret['traffic']['1day'] = self.m_zabbix_chart_traffic.format(str_graph_id, 60 * 60 * 24)
        self.m_dict_ret['traffic']['7day'] = self.m_zabbix_chart_traffic.format(str_graph_id, 60 * 60 * 24 * 7),

    def is_enable_args_format(self, *args, **kwargs):
        if len(args) == 1:
            return 1
        # 需要一个ip
        return 0

    def clear(self):
        self.__init__()

    def has_cache(self):
        if self.m_dict_ret['type'] == 'host' and self.m_object_key_store.has_key(self.m_dict_ret['ip']):
            return 1
        elif self.m_dict_ret['type'] == 'switch' and self.m_object_key_store.has_key(self.m_dict_ret['line']):
            return 1
        else:
            return 0

    def add_cache(self, json_chart_info):
        if not self.m_dict_ret['traffic']['graphid']:
            return
        if self.m_dict_ret['type'] == 'switch':
            dict_cache = {
                self.m_dict_ret['line']: json_chart_info
            }
        else:
            dict_cache = {
                self.m_dict_ret['ip']: json_chart_info
            }
        self.m_object_key_store.store(dict_cache)

    def read_cache(self):
        if self.m_dict_ret['type'] == 'switch':
            str_chart_info = self.m_object_key_store.key(self.m_dict_ret['line'])
        else:
            str_chart_info = self.m_object_key_store.key(self.m_dict_ret['ip'])
        dict_chart_info = ast.literal_eval(str_chart_info)
        json_chart_info = json.dumps(dict_chart_info)
        return json_chart_info

    def new_info(self):
        json_info = self.get_info()  # 使用强尧的查询接口查询该ip的相关信息
        str_traffic_url_demo = self.get_chart_url(json_info)  # 强尧的demo url，其中包含了图形对应的graph id
        self.get_graph_id(str_traffic_url_demo)
        self.assemble()
        json_chart_info = json.dumps(self.m_dict_ret)
        return json_chart_info

    def get(self, request, *args, **kwargs):
        self.clear()  # 清理上次执行时遗留的数据
        if not request.method == 'GET':  # and request.is_ajax():
            return HttpResponse()

        if not request.GET.get('ip'):
            return HttpResponse()

        self.m_dict_ret['ip'] = request.GET.get('ip')

        if self.m_dict_ret['ip'] in get_switch_map():
            self.m_dict_ret['type'] = 'switch'
            self.m_dict_ret['line'] = request.GET.get('line', None)  # 交换机的网口需要用线路信息来查找,不使用None则是null?
        else:
            self.m_dict_ret['type'] = 'host'
            self.m_dict_ret['interface'] = request.GET.get('interface', 'eth0')  # 当前用于adsl。默认值为eth0

        if self.has_cache():  # 检查是否有缓存数据可用。缓存可能导致数据不更新，需要删除缓存文件以让程序重新获得数据
            json_chart_info = self.read_cache()
            # print '使用缓存数据', json_chart_info
        else:
            json_chart_info = self.new_info()
            self.add_cache(json_chart_info)
        return HttpResponse(json_chart_info)

        # 报错文档：
        # 'str' object has no attribute 'get'
        # return 的必须是 HttpResponse()，其他django方法只是做了封装


if __name__ == '__main__':
    pass
