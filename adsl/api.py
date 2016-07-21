#<coding:utf-8>
def index(period='30day'):
	#from __future__ import division
	from main_switch import switch
	import os
	import time
	import json

	def getdata(rrdfile, period, endtime, cf):
	    command = '''rrdtool fetch --start="end - %s" --end="%s" -- %s %s''' %(period,endtime,rrdfile,cf)
	    #print command
	    try:
		rrdDATA = os.popen(command)
		rrdLine = rrdDATA.readlines()
		#print rrdLine
		rrdLine.pop(0)          # trafice_in trafic_out,这是os.popen命令多余的返回值
		rrdLine.pop(0)          # blank这是os.popen多余的返回值
		#print rrdLine
		data = [i.split() for i in rrdLine if "-nan" not in i]  # split()通过指定分隔符对字符串进行切片，默认为空格
		#data是一个嵌套的列表，得到这种格式是为了用for循环来遍历
		#print rrdLine
		if cf == 'MAX':
		    max1=0.0
		    max2=0.0
		    for j in data:
			#print j
		        data1 = float(j[1])
			#print j[1]
			#print float(j[1])
		        data2 = float(j[2])
			#print j[2]
			#print float(j[2])
		        if data1 > max1:   #获得traffic_in和traffic_out30天内的最大值
		            max1 = data1
		        if data2 > max2:
		            max2 = data2
		    return max([round(max1*8/1000/1000,2),round(max2*8/1000/1000,2)])  #将两个最大值进行比较，放回更大的
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
		    return max([round(8*sum1/count/1000/1000,2),round(8*sum2/count/1000/1000,2)])  #返回较大的值
	    except: 
	#        return [0,0]
		return 0

	cacti_rra_dir = '/var/lib/cacti/rra/'
	data_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	result_file = data_time + '.txt'
	now = int(time.time())


	#f = open(result_file,'w')
	result = {}
	for j in sorted(switch): #j表示机房
	    #print j
	    result[j] = {}
	    for i in switch[j]: #i表示线路
		#print i
		rrd_n = switch[j][i][0]#rrd文件的名字
		bound = switch[j][i][2]#带宽的大小
		rrdfile = cacti_rra_dir + str(rrd_n) #拼接得到完整的名字
		max2 = getdata(rrdfile,period,now,'MAX') #获得一个机房点
		tmp = {'used':max2,'total':bound}
		result[j][i] = tmp  #汉字被作为键值时，会存储其相对应的字符编码>>> print '\xe4\xb8\xad\xe5\xb1\xb1' ==>中山
		print result

	#f.close()
	json_data = json.dumps(result,sort_keys=True) #有sort_keys（对dict对象进行排序，我们知道默认dict是无序存放的）
	#json_data = result
	
	print json_data

index()
