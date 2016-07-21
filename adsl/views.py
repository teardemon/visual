# <coding:utf-8>
from django.shortcuts import render_to_response

from main_switch import switch
import os
import time
import json
from __future__ import division

def getdata(rrdfile, period, endtime, cf):
    command = '''rrdtool fetch --start="end - %s" --end="%s" -- %s %s''' % (period, endtime, rrdfile, 'MAX')
    try:
        rrdDATA = os.popen(command)
        rrdLine = rrdDATA.readlines()
        rrdLine.pop(0)  # trafice_in trafic_out
        rrdLine.pop(0)  # blank
        data1 = [i.split() for i in rrdLine if "-nan" not in i]  # select avaliable data
        data = [data1[-1], ]  # select avaliable data
        if cf == 'trafice_in':
            return round(float(data[0][1]) * 8 / 1000 / 1000, 2)
        elif cf == 'trafice_out':
            return round(float(data[0][2]) * 8 / 1000 / 1000, 2)
    except: 
#        return [0,0]
        return 0
		
def index(req):
	cacti_rra_dir = '/var/lib/cacti/rra/'
	data_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
	result_file = data_time + '.txt'
	
	now = int(time.time())
	a_week = now - 604800
	
	# f = open(result_file,'w')
	result = {}
	for j in switch:
	    if j.split('-')[1] == 'IN':
	        result[j] = {}
	        for i in switch[j]:
	            rrd_n = switch[j][i][0]
	            bound = switch[j][i][2]
	            rrdfile = cacti_rra_dir + str(rrd_n)
	            max2 = getdata(rrdfile, '1hour', now, 'trafice_in')
	            tmp = {'used':max2, 'total':bound}
	            result[j][i] = tmp
	    elif j.split('-')[1] == 'OUT':
	        result[j] = {}
	        for i in switch[j]:
	            rrd_n = switch[j][i][0]
	            bound = switch[j][i][2]
	            rrdfile = cacti_rra_dir + str(rrd_n)
	            max2 = getdata(rrdfile, '1hour', now, 'trafice_out')
	            tmp = {'used':max2, 'total':bound}
	            result[j][i] = tmp
	
	json_data = json.dumps(result, sort_keys=True)
	
	return render_to_response('idc.html', {'json_data':json_data})
