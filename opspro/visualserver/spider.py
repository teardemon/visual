# -*- coding:utf-8 -*-
# 作者：youzeshun
# 用途：urllib2封装

import urllib2
import json


# 返回的中文是unicode格式,print方法会自动将该格式按照当前系统的编码来转换
class CSpider:
    def init(self):
        pass

    def ReadRespond(self, sUrl):
        try:
            oResponse = urllib2.urlopen(sUrl)
        except:
            sResponse = ''
        else:
            sResponse = oResponse.read()
        return sResponse

    def ReadJson(self, sUrl):
        try:
            oResponse = urllib2.urlopen(sUrl)
        except:
            dResponse = {}
        else:
            dResponse = json.load(oResponse)
        return dResponse


if __name__ == '__main__':
    import idcconf

    g_oSpider = CSpider()


    def demo1():
        print g_oSpider.ReadRespond('http://10.32.18.176:8088/zapi/lastvalue/?id=2&ip=121.201.102.33')
        print g_oSpider.ReadJson('http://10.32.18.176:8088/zapi/lastvalue/?id=2&ip=121.201.102.33')


    def GetIPTop():
        jIPTop = g_oSpider.ReadJson(idcconf.URL_IDC_TOP)
        return eval(str(jIPTop))  # 先转json是为了避免中文未被编码。转dict是因为python遍历json对象有问题，目前没有定位问题。所以转为字典进行后续遍历


    def GetIDCTraff():
        jIDCTraff = g_oSpider.ReadJson(idcconf.URL_IDC_TRFF)
        return eval(str(jIDCTraff))
