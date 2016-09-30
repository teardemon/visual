#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-27 下午2:37
# @Author  : youzeshun
# 用于解决实时访问速度忙的问题。定时请求数据保存在文本中

import query
import json
from opspro.public.define import *
from opspro.visualserver.idcconf import *


def CacheQuery():
    jIDCTraff = query.GetIDCTraff()
    if not jIDCTraff:
        str_msg = 'IDC线路流量不允许为空.\n请手动核对接口数据：{0}'.format(URL_IDC_TRFF)
        ExecManagerFunc('log', 'Log', str_msg, 'status/error')
        ExecManagerFunc('alert', 'Alert', 'IDC线路流量不允许为空', [YouZeShun, ChenWuJie, QiangYao])

    jIPTop = query.GetIPTop()
    if not jIPTop:
        str_msg = '机房 所有 Top10流量为空.\n可能原因：\n1.数据端负载高，导致请求超时\n2.数据的来源异常。\n请手动核对接口数据：{0}'.format(URL_IDC_TOP)
        ExecManagerFunc('log', 'Log', str_msg, 'status/error')
        ExecManagerFunc('alert', 'Alert', str_msg, [YouZeShun, ChenWuJie, QiangYao])

    dDataEchart, dOtherUsedBand = query.GetDataEchart(jIDCTraff, jIPTop)
    dDataEchart = query.AddOuterItem(dDataEchart, dOtherUsedBand)
    dDataEchart = query.LineOrder(dDataEchart)  # 为线路的先后顺序进行排序
    if not dDataEchart:
        ExecManagerFunc('alert', 'Alert', 'opspro没能生成echart数据！idc流量图将无法刷新！', 8766)
        ExecManagerFunc('log', 'Log', 'opspro没能生成echart数据！idc流量图将无法刷新！', 'error/level1')
        return

    # json.dumps()将原本的Unicode字符拆分成一个个单独的ASCII码，ensure_ascii=False将不拆分.
    # 这样能以中文字符的形式将数据写到文本中，但是数据由于不是python能识别的编码，在未知情况下会报错
    dDataCache = {
        'date': GetTime(),
        'data': dDataEchart
    }
    # jResponse = json.dumps(dDataEchart, ensure_ascii=False)
    jResponse = json.dumps(dDataCache)
    # 由于Unicode字符没被拆分为ascll码，不能被python的函数ushi用。需用进行编码
    jResponse = jResponse.encode('utf-8')
    # 注意权限！
    ExecManagerFunc('log', 'Cache', jResponse, '../../static/idc/cache/pie.json')


# 周期性地调用缓存代码
def PeriodCache():
    CacheQuery()
    Remove_Call_Out("periodcache")
    Call_Out(PeriodCache, 30, "periodcache")  # 为了不重名，使用文件名作为注册名
