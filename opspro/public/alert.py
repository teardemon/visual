# -*- coding: utf-8 -*-
'''
用于im火星报警
*变动记录：
    1.保持调用方式的简洁，允许传列表
    2.保持内部结构的简洁，当调用错误通过火星发送通知而不在记录错误

测试指令：
	 python opspro/debugals.py --mod=alert --func=Alert --argv=8766,ff
'''
from define import *
import terminal
import os

g_SpecialSymbol = {
    # '%':'%25',这个符号必须单独进行替换
    '+': '%2B',
    ' ': '%20',
    '/': '%2F',
    '?': '%3F',
    '#': '%23',
    '&': '%26',
    '\n': '%0a',
    '=': '%3D',
}


# 一些在url出现的字符必须被过滤掉，比如空格等
def ContentFilter(sContent):
    if not isinstance(sContent, str):
        return sContent  # 只有字符串才需要进行编码的检查
    sContent = sContent.replace('%', '%25')  # 单独替换百分号，然后再遍历替换其他特殊符号。否则其他符号会被百分号替换掉
    for sSpecialSymbol, sUrlEncoding in g_SpecialSymbol.items():
        sContent = sContent.replace(sSpecialSymbol, sUrlEncoding)
    return sContent


def GetAlertUrl(sContent, sIMNumber):
    sIMNumber = str(sIMNumber)
    sContent = str(sContent)
    sUrl = "http://im.2980.com:8088/sendmsg?key=public_server_waring&accounts=%s&content=%s" % (sIMNumber, sContent)
    return sUrl


# 基于wget命令的报警，需在linux中使用。
# wget对一些特殊符号会出现报警不正常的情况
def AlertLinux(sContent, sIMNumber):
    sEncodingContent = ContentFilter(sContent)
    sUrl = GetAlertUrl(sEncodingContent, sIMNumber)
    # --quiet 安静模式，--spider 不下载  --tries表示报警次数  & 后台进行，当网络不可访问的时候不会引起阻塞
    # 可能是wget命令的bug。当使用--tries部分报价会失败
    sShellCmd = "wget --quiet -O /dev/null '%s' &" % (sUrl)
    os.popen(sShellCmd)


# 解决重复报警的问题
class CAlertManager(object):
    def __init__(self):
        self.m_AlertRecord = {}

    def Register(self, sAlertMsg):
        iTime = GetSecond('us')  # 这个单位一定要非常小，小到即使连续执行报警，也不会发生键名重复
        self.m_AlertRecord[iTime] = sAlertMsg

    def IsReAlert(self, sNameRegister):
        for k, v in self.m_AlertRecord.items():
            if sNameRegister == v:
                return 1
        return 0

    def UpdateRecord(self, iInterval):
        iNowTime = GetSecond('us')
        dTmp = {}
        for k, v in self.m_AlertRecord.items():
            if iNowTime - k < iInterval * 1000 * 1000:  # 必须换算到纳秒进行比较
                dTmp[k] = v
        self.m_AlertRecord = dTmp

    def AlertToOne(self, AlertMsg, IMNumber, iInterval=TIME_REALERT):
        '''
        @param AlertMsg: 报警的内容
        @param IMNumber: 报警的火星号码：字符串 or 整型
        @param iInterval: 多少s内报过，则这次不报。默认１０分钟。即这次报警的内容在１０分钟内报过这次不会报警
        @return:
        '''
        sIP = terminal.RunCmd('ip')
        if not isinstance(IMNumber, int) and not isinstance(IMNumber, str):
            sMsg = '{0} 方法使用错误：CAlertManager.AlertToOne(报警内容,字符串或整型的火星号).传入了错误的类型：{0},值：{1}'.format(sIP, type(IMNumber),
                                                                                                    IMNumber)
            AlertLinux(sMsg, YouZeShun)
            return
        sAlertMsg = '【来自:{0}】 {1}'.format(sIP, AlertMsg)
        self.UpdateRecord(iInterval)  # 删除10分钟以前尝试的报警记录
        sNameRegister = str(IMNumber) + sAlertMsg  # 相同的报警是发给相同火星号的相同消息
        if self.IsReAlert(sNameRegister):
            return
        self.Register(sNameRegister)
        AlertLinux(sAlertMsg, IMNumber)

    def AlertToMany(self, AlertMsg, lstIMNumber, iInterval=TIME_REALERT):
        for IMNumber in lstIMNumber:
            self.AlertToOne(AlertMsg, IMNumber)

    def Alert(self, AlertMsg, IMNumber, iInterval=TIME_REALERT):
        if isinstance(IMNumber, str) or isinstance(IMNumber, int):
            self.AlertToOne(AlertMsg, IMNumber, iInterval)
        if isinstance(IMNumber, list):
            self.AlertToMany(AlertMsg, IMNumber, iInterval)


if __name__ == '__main__':
    def demo1():
        '''
        最简易的报警
        @return:
        '''
        AlertLinux('报警内容', 8766)


    def demo2():
        oAlert = CAlertManager()
        oAlert.AlertToOne('报警内容', 8766)


    def demo3():
        '''
        限制重复报警
        @return:
        '''
        oAlert = CAlertManager()
        oAlert.AlertToOne('报警内容', 8766)
        oAlert.AlertToOne('报警内容', 8766)  # 这次不会报出
        oAlert.AlertToOne('报警内容', 8766, 0)  # 这次会报出(火星报警有限制策略，这条报警实际不会收到)
