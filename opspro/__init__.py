#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-9-2 上午10:59
# @Author  : youzeshun
# 导入模块的版本：
# 参考资料  :
# 说明     :
import public
import visualserver


def Init():
    sPathOpspro = public.path.GetCurPath(__file__, -1)
    visualserver.Init(sPathOpspro, sPathOpspro)


def Start():
    visualserver.Start()


Init()
