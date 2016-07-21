#<coding:utf-8>
debug=0

if ((debug==1)):
	standardLoss=5    #为了能明显的看到现象，在丢包小于1%时就显示
	nagiosTotalPath='/var/www/html/mysite/static/pingMap/data/nagiosData.txt'
	nagiosDxPath='/var/www/html/mysite/static/pingMap/data/nagiosDx.txt'
	nagiosWtPath='/var/www/html/mysite/static/pingMap/data/nagiosWt.txt'
	nagiosTotalLossPath='/var/www/html/mysite/static/pingMap/data/nagiosLossData.txt'
	nagiosDxLossPath='/var/www/html/mysite/static/pingMap/data/nagiosDxLoss.txt'
	nagiosWtLossPath='/var/www/html/mysite/static/pingMap/data/nagiosWtLoss.txt'
else:
    standardLoss=5
    nagiosTotalPath='/var/www/mysite/static/pingMap/data/nagiosData.txt'
    nagiosDxPath='/var/www/mysite/static/pingMap/data/nagiosDx.txt'
    nagiosWtPath='/var/www/mysite/static/pingMap/data/nagiosWt.txt'
    nagiosTotalLossPath='/var/www/mysite/static/pingMap/data/nagiosLossData.txt'
    nagiosDxLossPath='/var/www/mysite/static/pingMap/data/nagiosDxLoss.txt'
    nagiosWtLossPath='/var/www/mysite/static/pingMap/data/nagiosWtLoss.txt'

BGP=['220.231.248.81']
