#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2

dic={"电信":"DX","网通":"WT"}

interface='http://192.168.165.126:93/daochu/jiankongshuju_two.aspx'
rawdata=urllib2.urlopen(interface).read()
datalist=rawdata.split('\n')
host_city={}
line_type={}

for i in range(len(datalist)):
	if datalist[i]=='':
		del datalist[i]	

for host in datalist:
	type=host.split()[2][0:6]
	line_type[host.split()[0]]=dic[type]
	host_city[host.split()[0]]=host.split()[1]
line_type['220.231.248.81']='BGP'
