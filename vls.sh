#/bin/dash
#Created on 2016-9-5
#@author: cwj
#用途：
#	启动关闭Django服务


Stop(){

	#第一个.*表示manage.py所在的路径
	#第二个.*表示ip访问
	if [ -z "$num" ];then
		echo '需要端口号'
		exit 0
	fi
	ps aux|grep -e 'python.*manage.py *runserver'.*$num|awk '{print $2}'|xargs sudo kill
}

Start(){
	if [ -z "$num" ];then
		echo '需要端口号'
		exit 0
	fi

	tmp1=`netstat -anp|awk '{print $4}'|awk -F ':' '{print $2}'|grep -v '^$'`
	for var in $tmp1
	do 
	if [ $var = $num ];then
		echo '端口被占用'
		exit 0
	fi
	done
	echo "nohup python ${basePath}/manage.py runserver 0.0.0.0:$num &> "${basePath}/data/log/django.log" &"
	nohup python ${basePath}/manage.py runserver 0.0.0.0:$num &> "${basePath}/data/log/django.log" &
}

Status(){
	tmp2=$(ps aux|grep -e "python.*${basePath}/manage.py *runserver"|awk {'print $14'}|awk -F ':' {'print $2'}|head -n 1)
	if [ ! $tmp2 ];then
		echo '服务未启动'
		exit 0
	else
		echo '服务已启动，端口号为'$tmp2
		exit 0
	fi
}

Tip(){
	echo "语法：bash vls.sh start|stop|restart|status Mode port_number
	例如：
	启动服务：bash vls.sh start 80
	结束服务：bash vls.sh stop 80
	重启服务:bash vls.sh restart 80
	查看服务状态:bash vls.sh status"
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
		status)
			Status
		;;
		*)
			echo '没有这个动作，start|restart|stop|status'
			Tip
			exit
		;;
	esac
} 

Init
Main $@