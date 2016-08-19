# <coding:utf-8>
from django.shortcuts import HttpResponse
from django.views.generic import View

import spider
import re
import json
import yaml


class CZabbix(View, spider.CSpider):
    m_api_zabbix_info = 'http://10.32.18.176:8088/zapi/graph/?id=123&ip={0}'
    m_api_zabbix_chart = 'http://10.32.64.64/zabbix/chart2.php?graphid={0}&period={1}&updateProfile=1&profileIdx=web.screens&width=700'
    m_dict_map = yaml.load(file('static/idc/cache/ip_to_interface.yaml'))

    def get_host_info(self, *args):
        str_api_url_zabbix = self.m_api_zabbix_info.format(*args)
        json_host_info = self.ReadJson(str_api_url_zabbix)
        return json_host_info

    def get_server_chart_url(self, list_ret):
        for dict_item in list_ret:
            if 'Traffic on interface eth0' in dict_item:
                str_url = dict_item['Traffic on interface eth0']
                return str_url
        return ''

    def get_switch_chart_url(self, list_ret, str_ip):
        if not str_ip in self.m_dict_map:
            # 未知的ip，可能是交换机的ip换过了
            return
        str_interface = self.m_dict_map[str_ip]
        for dict_interface_url in list_ret:
            for str_full_interface, str_url in dict_interface_url.iteritems():
                if str_interface in str_full_interface:
                    return str_url

    def get_chart_url(self, json_host_info, *args):
        if not json_host_info:
            return ''
        # ret 可能是列表或字典
        ret = json_host_info['result']
        if isinstance(ret, dict):
            # 字典说明错了
            return ''
        str_server_chart_url = self.get_server_chart_url(ret)
        if str_server_chart_url:
            return str_server_chart_url
        str_switch_chart_url = self.get_switch_chart_url(ret, *args)
        return str_switch_chart_url

    # http://10.32.64.64/zabbix/chart2.php?graphid=50832&period=3600&updateProfile=1&profileIdx=web.screens&width=600
    def get_graph_id(self, str_chart_url):
        if not str_chart_url:
            return ''
        object_ret = re.search('(?<=graphid=)\d+', str_chart_url)
        if object_ret:
            return object_ret.group(0)
        return ''

    def assemble(self, str_graph_id):
        if not str_graph_id:
            return ''
        dict_url = {
            '1day': self.m_api_zabbix_chart.format(str_graph_id, 60 * 60 * 24),
            '7day': self.m_api_zabbix_chart.format(str_graph_id, 60 * 60 * 24 * 7)
        }
        return dict_url

    def get(self, request, *args, **kwargs):
        json_host_info = self.get_host_info(*args)
        # 预计返回值：
        # http://10.32.64.64/zabbix/chart2.php?graphid=50832&period=3600&updateProfile=1&profileIdx=web.screens&width=900
        str_chart_url = self.get_chart_url(json_host_info, *args)
        str_graph_id = self.get_graph_id(str_chart_url)
        dict_url = self.assemble(str_graph_id)
        json_url = json.dumps(dict_url)
        return HttpResponse(json_url)
