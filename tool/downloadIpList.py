#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import subprocess
from conf import BGP
rawdata=subprocess.check_output('curl -s  http://192.168.165.126:93/daochu/jiankongshuju_two.aspx|awk -F"[- ]" \'{print $1" "$2""$3"-"$4" "$5}\'', shell=True)
datalist=rawdata.split('\n')
for i in range(len(datalist)):
    if datalist[i]=='':
            del datalist[i]
for i in datalist:
    print i
host_city={}
DX={}
WT={}
for host in datalist:
    host_city[host.split()[0]]=host.split()[1]
    if host.split()[1].split('-')[1][0:6]=='电信':
	DX[host.split()[0]]=host.split()[1]
    else:
	WT[host.split()[0]]=host.split()[1]

for ip in BGP:
	if ip not in WT:
		WT[ip]=host_city[ip]
	if ip not in DX:
		DX[ip]=host_city[ip]
	

