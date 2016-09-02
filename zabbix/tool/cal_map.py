#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-8-19 下午7:57
# @Author  : youzeshun
# 参考资料  :
# 说明     :交换机网口和ip的对应关系由强尧维护，该代码用以计算出本django程序所需要的yaml文件
import yaml
from opspro.public import spider


def static():
    object_yaml = yaml.load(file('switch.yaml'))

    dict_ret = {}

    for str_server_room, dict_line in object_yaml.iteritems():
        for k, v in dict_line.iteritems():
            print k, v[0], v[1]
            if not dict_ret.has_key(v[0]):
                dict_ret[v[0]] = {}
            dict_ret[v[0]][k] = v[1]
    print dict_ret

    object_file = open('ip_to_interface.yaml', 'w')
    yaml.dump(dict_ret, object_file, encoding='utf-8', allow_unicode=True)
    object_file.close()


def dynamic(str_path='ip_to_interface.yaml'):
    str_url = 'http://10.32.64.64:8000/info/getidc/'
    object_spider = spider.CSpider()
    json_map_info = object_spider.ReadJson(str_url)
    dict_ret = {}
    for str_server_room, dict_line in json_map_info.iteritems():
        for str_line_name, dict_line_info in dict_line.iteritems():
            if not dict_line_info.has_key(u'ip') or not dict_line_info.has_key(u'interface'):
                print '意料之外的情况:字典{0}信息不全'.format(dict_line_info)
                return
            str_interface = dict_line_info['interface']
            str_ip = dict_line_info['ip']
            if not dict_ret.has_key(dict_line_info['ip']):
                dict_ret[str_ip] = {}
            dict_ret[str_ip][str_line_name] = str_interface
    object_file = open(str_path, 'w')
    yaml.dump(dict_ret, object_file, encoding='utf-8', allow_unicode=True)
    object_file.close()


if __name__ == '__main__':
    dynamic()
