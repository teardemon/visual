function showLossPacket(){
	//由于暂时没弄明白如何定义两处静态目录，数据线暂时放这
	nagiosLossData=getJsonFileContent("/static/pingMap/data/nagiosLossData.txt");
	host_city=nagiosLossData.host_city
	network_data=nagiosLossData.data
	//nagiosServerIp:{nagiosServerIp:{"rta": "", "lost": ""},... ...}
	markLine_data=[]
	var errorItem=''
	for (var nagiosServerIp in network_data){
		for (var nagiosClientIp in network_data[nagiosServerIp]){
			if (network_data[nagiosServerIp][nagiosClientIp]==null){
				console.log("nagiosServer:"+nagiosServerIp+" nagiosClientIp"+nagiosClientIp+"缺少网络状况信息")
				continue
			}
			errorItem+="<thead><tr><th>"+ host_city[nagiosServerIp]  +"</th><th>"+ host_city[nagiosClientIp] +"</th><th>"+ network_data[nagiosServerIp][nagiosClientIp]["lost"] +"</th><th>"+network_data[nagiosServerIp][nagiosClientIp]["rta"] +"</th></tr></thead>"
		}
	}
	error_text = "<thead><tr><th>来源</th><th>目的</th><th>丢包</th><th>延迟</th></tr></thead>"+errorItem;
	$("#text_area").empty();
	$("#text_area").append(error_text);
}
