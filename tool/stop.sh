#!/usr/bin/env bash
#如果有多个项目怎么办
if [ -z "$1" ];then
    echo '需要端口号'
    exit 0
fi

#第一个.*表示manage.py所在的路径
#第二个.*表示ip访问
ps aux|grep -e 'python.*manage.py *runserver'.*$1|awk '{print $2}'|xargs sudo kill
