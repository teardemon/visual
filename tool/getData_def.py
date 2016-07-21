#!/usr/bin/env python
#<coding:utf-8>

import json
import requests
from concurrent.futures import ThreadPoolExecutor

def deal_host_status(host_status):
    key_words = ["hoststatus","plugin_output"]
    result = {}
    flag = 0
    for i in host_status:
        if key_words[0] in i:
            pef_data_dic={}
            flag = 1
        elif flag and 'localhost' in i:  # filter localhost
            flag =0
        elif flag and (key_words[1] in i):
            flag = 0
            tmp = i.strip().split(':')  #plugin_output=OK - 219.132.195.81: rta 4.624ms, lost 0%
            if ((len(tmp) == 2)):
                dst_host = tmp[0].strip().split()[-1].strip()
                pef_data = tmp[1].strip().split(',')
                pef_data_rta = pef_data[0].split()[-1]      # rta
                pef_data_pl = pef_data[1].split()[-1]       # package lost
                pef_data_dic["rta"],pef_data_dic["lost"]  = pef_data_rta,pef_data_pl
                result[dst_host]=pef_data_dic
    return result

def get_host_status(host_ip):           
    host_url = "http://%s/status.txt" %host_ip
    try:
        host_status = requests.get(host_url,timeout=1).content.split('\n')
    except :
        return None
    return  deal_host_status(host_status)
    
def getdata(serverIp):
        with ThreadPoolExecutor(max_workers=20) as executor:
                results = dict((ip,executor.submit(get_host_status,ip)) for ip in serverIp.keys())
        for i in results:
                results[i] = results[i].result()
        for k,v in results.items():
                if not v:
                        results.pop(k)
                        del serverIp[k]
        info_results={}
        for nagiosServerIp1 in serverIp.keys():
                info={}
                for nagiosServerIp2 in serverIp.keys():
                        info[nagiosServerIp2]=results.get(nagiosServerIp1).get(nagiosServerIp2)
                info_results[nagiosServerIp1]=info
        return info_results


def writeFile(path,value):
        with open(path,'w+') as f:
                f.write(value)
                f.close()

def alert(results,standardLoss):
        nagiosWarn=[]
        for nagiosServerIp in results.keys():
        	for nagiosClientIp in results[nagiosServerIp].keys():
			if not results[nagiosServerIp][nagiosClientIp]:
				continue
			if int(results[nagiosServerIp][nagiosClientIp]['lost'][:-1])<=standardLoss:
                        		del results[nagiosServerIp][nagiosClientIp]


