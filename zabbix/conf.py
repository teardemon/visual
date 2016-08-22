#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-8-22 下午3:42
# @Author  : youzeshun
# 参考资料  :
# 说明     :
import yaml


# 交换机ip和端口的映射 ， 该参数不允许类修改，只允许访问
def get_switch_map():
    object_file = file('static/idc/cache/ip_to_interface.yaml')
    dict_switch_map = yaml.load(object_file)
    return dict_switch_map.copy()


DICT_SWITCH_MAP = get_switch_map()

if __name__ == '__main__':
    pass
