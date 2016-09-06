#/bin/dash
'''
Created on 2016-9-5
@author: cwj
用途：
	启动关闭Django服务

'''
Stop(){
	if [ -z "$num" ];then
		echo '需要端口号'
		exit 0
	fi

	#第一个.*表示manage.py所在的路径
	#第二个.*表示ip访问
	ps aux|grep -e 'python.*manage.py *runserver'.*$1|awk '{print $2}'|xargs sudo kill
}

Start(){
	if [ -z "$num" ];then
		echo '需要端口号'
		exit 0
	fi

	tmp=$(netstat -anp|grep tcp|cut -c 21-42|cut -d ':' -f 2|grep $num)
	for var in $tmp
	do 
	if [ "$var"=="$num" ];then
		echo '端口被占用'
		exit 0
	fi
	done
	python manage.py runserver 0.0.0.0:$num &> "${basePath}/data/log/django.log"
}

Tip(){
	echo "语法：bash vls.sh start|stop|restart Mode port_number
	例如：
	启动服务：bash vls.sh start 80
	结束服务：bash vls.sh stop 80
	重启服务:bash vls.sh restart 80"
}

Init(){
	basePath=$(cd `dirname $0`;pwd)
}

Main(){
	mode=$1
	num=$2
	case $mode in
		start)
			Start
		;;
		stop)
			Stop
		;;
		restart)
			Stop
			Start
		;;
		*)
			echo '没有这个动作，start|restart|stop'
			Tip
			exit
		;;
	esac
} 

Init
Main $@