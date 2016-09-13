#!/usr/bin/env bash
#basePath=$(cd `dirname $0`;pwd)
#. $basePath/etConf.sh
passphrase='123456'
key='/home/yzs/.ssh/youzeshun'
user='youzeshun'

ip="192.168.165.200"
cmd="$2"
port="82"

/usr/bin/expect -c "set timeout 5
        spawn  ssh -p 45222 -i ${key}  ${user}@"$ip" -o StrictHostKeyChecking=no
        expect \"Enter passphrase for key\" {send \"${passphrase}\n\"}
        expect \"${user}@debian\" {send \"${cmd}\n\"}
        expect \"${user}@debian\" {send \"su ops\n\"}
        expect \"Password:\" {send \"ops\n\"}
        expect \"ops@debian\" {send \"sudo dash /opt/visual/vls.sh start ${port}\n\"}
        expect \"password for\" {send \"ops\n\"}
    expect eof
"