#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-10-14 上午11:09
# @Author  : youzeshun
# 导入模块的版本：
# 参考资料  :
# 说明     :
# -*- coding:utf-8 -*-

import getopt
import sys
import opspro


def GetOpt():
    lstOpt, lstArgs = getopt.getopt(sys.argv[1:], '', ['logpath=', 'rootpath=', ])
    # 参数的解析过程,长参数为--，短参数为-
    for sOption, sValue in lstOpt:
        if sOption in ["--logpath"]:
            sLogPath = sValue
        elif sOption in ["--rootpath"]:
            sRootPath = sValue

    if not locals().has_key('sLogPath'):
        raise UnboundLocalError("必须设置日志的路径")
    if not locals().has_key('sLogPath'):
        raise UnboundLocalError("必须设置程序的根路径(用于python调用shell脚本)")

    return sLogPath, sRootPath


if __name__ == '__main__':
    sLogPath, sRootPath = GetOpt()
    opspro.Init(sLogPath, sRootPath)
    opspro.Start(sLogPath, sRootPath)
