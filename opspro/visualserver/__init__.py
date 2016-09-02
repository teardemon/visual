#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-7-25 下午2:58
# @Author  : youzeshun
import cache
import query
import api
from opspro.public import timerctrl
from opspro.public import rwtext
from opspro.public import alert
from opspro.public import keycache
from opspro.public.define import *


def Init(sLogPath, sRootPath):
    SetGlobalManager('rootpath', sRootPath)  # 脚本的根路径，用于寻找资源
    SetGlobalManager('log', rwtext.CRWText(sLogPath))
    SetGlobalManager("timer", timerctrl.CTimerManager())
    SetGlobalManager("alert", alert.CAlertManager())
    SetGlobalManager("cache", keycache.CKeyStore('{0}/{1}'.format(sLogPath, 'top.cache')))


def Start():
    cache.PeriodCache()
