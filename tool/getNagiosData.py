#<coding:utf-8>
#!/usr/bin/env python
import json
import getData_def
from downloadIpList import host_city,DX,WT
from conf import nagiosTotalLossPath,nagiosDxLossPath,nagiosWtLossPath 
from conf import nagiosTotalPath,nagiosDxPath,nagiosWtPath,standardLoss
 
#total_results=getData_def.getdata(host_city)
DX_results=getData_def.getdata(DX)
WT_results=getData_def.getdata(WT)

DX_data={}
WT_data={}
total_data={}

total_results={}
for m in DX_results:
    total_results[m]=DX_results[m]
for n in WT_results:
    total_results[n]=WT_results[n]
total_data["data"],total_data["host_city"]= total_results,host_city
#DX_data["data"],DX_data["host_city"]= DX_results,DX
#WT_data["data"],WT_data["host_city"]= WT_results,WT

#DX_status = json.dumps(DX_data)
#WT_status = json.dumps(WT_data)
total_status = json.dumps(total_data)

getData_def.writeFile(nagiosTotalPath,total_status)
#getData_def.writeFile(nagiosDxPath,DX_status)
#getData_def.writeFile(nagiosWtPath,WT_status)



getData_def.alert(total_results,standardLoss)
#getData_def.alert(DX_results,standardLoss)
#getData_def.alert(WT_results,standardLoss)

TotalLoss={}
#DxLoss={}
#WtLoss={}

TotalLoss["data"],TotalLoss["host_city"]= total_results,host_city
#DxLoss["data"],DxLoss["host_city"]= DX_results,DX
#WtLoss["data"],WtLoss["host_city"]= WT_results,WT

nagiosTotalLoss = json.dumps(TotalLoss)
#nagiosDxLoss = json.dumps(DxLoss)
#nagiosWtLoss = json.dumps(WtLoss)

getData_def.writeFile(nagiosTotalLossPath,nagiosTotalLoss)
#getData_def.writeFile(nagiosDxLossPath,nagiosDxLoss)
#getData_def.writeFile(nagiosWtLossPath,nagiosWtLoss)




