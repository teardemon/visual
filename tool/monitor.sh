#!/usr/bin/env bash
#  作者：yzs
#  用途：检查可视化程序是否在运行，检查可视化程序数据源是否及时更新
#  使用方式：
#  root权限－计划任务
#  0 0 * * * /usr/sbin/ntpdate time.nist.gov
#  */1 * * * * dash /home/yzs/visual/monitor.sh

startup(){
    basePath=$(cd `dirname $0`;pwd)
    source ${basePath}/remote_start.sh
}

Alert(){
wget --quiet -O /dev/null "http://im.2980.com:8088/sendmsg?key=public_server_waring&accounts=8766&content="${1} &
}

type jq || apt-get install jq -y
type jq || exit

type curl || apt-get install curl -y
type curl || exit

sPort="82"
sFile="/static/idc/cache/pie.json"
sWebsite="http://192.168.165.200:${sPort}"
sUrl="${sWebsite}${sFile}"
#返回带有date字段的json数据则为０
date=`curl -s "${sUrl}"|jq '.date'`
bSuccess=$?

# date为空说明jq没有输入（服务可能没有启动）
if [ -z "${date}" ]
then
    Alert "流量可视化(${sWebsite}):已停止！请重启django"
    startup
    exit
elif [ ! "${bSuccess}" -eq 0 ]
then
    # data有值，值可能不是时间。此时jq会过滤出错，bSuccess不等于０
    Alert "不能获得文件:"${sUrl}"无法判断页面数据源是否超时未刷新"
    exit
fi

#获得date字段中冒号内的值，无论是否获得$?都为０
date=`echo $date|awk -F"\"" '{print $2}'`
iDataTime=`date -d "${date}" +%s`
iNowTime=`date +%s`
mistiming=`echo ${iNowTime}-${iDataTime}|bc`

if [ "${mistiming}" -gt 60 ]
then
    Alert "流量可视化(${sWebsite}):idc页面数据源超过60s没有刷新!"
    exit
fi

#echo "数据源的时间 "${date}
#echo "本地时间和数据源的时间差 "${mistiming}
