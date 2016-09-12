#!/usr/bin/env bash
#  作者：yzs
#  用途：检查可视化程序是否在运行，检查可视化程序数据源是否及时更新
Alert(){
wget --quiet -O /dev/null "http://im.2980.com:8088/sendmsg?key=public_server_waring&accounts=8766&content="${1} &
}

type jq || apt-get install jq -y
type jq || exit

type curl || apt-get install curl -y
type curl || exit

#返回带有date字段的json数据则为０
date=`curl -s  http://192.168.165.200:82/static/idc/cache/pie.json|jq '.date'`
bSuccess=$?
if [ ! "${bSuccess=}" -eq 0 ]
then
    # 火星短信报警
    Alert "流量可视化:82端口已停止！请重启django"
    exit
fi

#获得date字段中冒号内的值，无论是否获得$?都为０
date=`echo $date|awk -F"\"" '{print $2}'`
iDataTime=`date -d "${date}" +%s`
iNowTime=`date +%s`
mistiming=`echo ${iNowTime}-${iDataTime}|bc`

if [ "${mistiming}" -gt 60 ]
then
    Alert "流量可视化:idc页面数据源超过60s没有刷新!"
    exit
fi
