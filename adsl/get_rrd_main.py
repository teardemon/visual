#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from __future__ import division
from main_switch import switch
import os
import time
import json

def getdata(rrdfile, period, endtime, cf):
    command = '''rrdtool fetch --start="end - %s" --end="%s" -- %s %s''' %(period,endtime,rrdfile,cf)
    try:
        rrdDATA = os.popen(command)
        rrdLine = rrdDATA.readlines()
        rrdLine.pop(0)          # trafice_in trafic_out
        rrdLine.pop(0)          # blank
        data1 = [i.split() for i in rrdLine if "-nan" not in i]  # select avaliable data
        data = [data1[-1],]  # select avaliable data
        if cf == 'MAX':
            max1=0.0
            max2=0.0
            for j in data:
                data1 = float(j[1])
                data2 = float(j[2])
                if data1 > max1:
                    max1 = data1
                if data2 > max2:
                    max2 = data2
            return max([round(max1*8/1000/1000,2),round(max2*8/1000/1000,2)])
        elif cf == 'AVERAGE':
            sum1 = 0.0
            sum2 = 0.0
            count =1
            for j in data:
                data1 = float(j[1])
                data2 = float(j[2])
                sum1 = sum1 + data1
                sum2 = sum2 + data2
                count = count +1
            return max([round(8*sum1/count/1000/1000,2),round(8*sum2/count/1000/1000,2)])
    except: 
#        return [0,0]
        return 0

cacti_rra_dir = '/var/lib/cacti/rra/'
data_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
result_file = data_time + '.txt'

now = int(time.time())
a_week = now - 604800

#f = open(result_file,'w')
result = {}
for j in switch:
    result[j] = {}
    for i in switch[j]:
        rrd_n = switch[j][i][0]
        bound = switch[j][i][2]
        rrdfile = cacti_rra_dir + str(rrd_n)
    #    max1 = getdata(rrdfile,'1day',now,'MAX') * 100
        max2 = getdata(rrdfile,'1hour',now,'MAX')
    #    max2 = getdata(rrdfile,'7day',now,'MAX')
        tmp = {'used':max2,'total':bound}
        result[j][i] = tmp
    #    max3 = getdata(rrdfile,'7day',a_week,'MAX') * 100
    #    max4 = getdata(rrdfile,'30day',now,'MAX') * 100
    #    average1 = getdata(rrdfile,'1day',now,'AVERAGE') * 100
    #    average2 = getdata(rrdfile,'7day',now,'AVERAGE') * 100
    #    average3 = getdata(rrdfile,'7day',a_week,'AVERAGE') * 100
    #    average4 = getdata(rrdfile,'30day',now,'AVERAGE') * 100
    #    content = '%s :\t%s\t%s\n' %(i,max2,bound)   
    #    f.write(content)


#f.close()
json_data = json.dumps(result,sort_keys=True)
print json_data
