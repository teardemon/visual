#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-9-2 上午10:59
# @Author  : youzeshun
# 导入模块的版本：
# 参考资料  :
# 说明     :
import public
import visualserver


def Init(sLogPath='', sRootPath=''):
    sLogPath = sLogPath if sLogPath else public.path.GetCurPath(__file__, -1)
    visualserver.Init(sLogPath, sRootPath)


def Start(sLogPath, sRootPath):
    visualserver.Start(sLogPath, sRootPath)


Init()
