function drawChart(serverLine, idc_used, idc_total) {
	var non_used = parseFloat((idc_total - idc_used).toFixed(10));
	option = getOption(idc_used, idc_total);//获得用于配置的option
	baiduEcharts('echarts/chart/pie',option);//指定echarts模块类型，同时option将其用于绘图

	function getOption(idc_used,idc_total) {
		if (non_used < 0) {
			non_used = 0; //网络攻击等情况下，数据包总量是可以超过带宽最大值的，虽然包会丢失
		}

		if ((idc_used / idc_total) > 0.9) 
			var idc_used_color = '#FF0000'; //'#FF0000' red
		else if ((idc_used / idc_total) > 0.7) 
			var idc_used_color = '#FF8C00'; //'#FF8C00'chengse
		else 
			var idc_used_color = '#32cd32'; //'#32cd32' green

		var option = {
			color: [idc_used_color, '#999999'],//染色的对象是所在函数的参数getOption(idc_used,idc_total)
			title: {
				text: serverLine,
				//显示未用，以检查计算错误
				subtext: '总带宽: ' + idc_total + 'Mb/s\n' + '已用: ' + idc_used + 'M/s',//\n'+'未用:'+non_used+ 'M/s',
				x: 'center',
				textStyle:{
					fontSize:32
				}
			},
			tooltip: {
				trigger: 'item',
				formatter: "{b} : {c} ({d}%)" //聚焦时，弹出的显示框的格式
			},
			series: [{
				center: ['50%', '63%'],
				//图像的坐标，默认50%,50%
				type: 'pie',
				//显示的图形，需要加载相应文件
				radius: '68%',
				//图像的比例
				data: [{
					value: idc_used,
					name: '已用'
				},
				{
					value: non_used,
					name: '未用'
				}],
				itemStyle: {
					normal: {
						label: {
							show: true,
							position: 'inner',
							formatter: "{b}\n{d}%" //当不聚焦在图形上时,显示的格式
						},
						labelLine: {
							show: false
						} //是否显示小把手
					},
					emphasis: {
						label: {
							show: true,
							//当聚焦在图形上时,是否显示
							formatter: "{b}\n{d}%" //当聚焦在图形上时,显示的格式
						}
					}
				}
			}]
		}
		return option
	}

	function baiduEcharts(module,option) {
		// 路径配置
		require.config({
			paths: {
				echarts: '/static/public/js/echarts/2.2.7/build/dist'
			}
		});
		// 在上述路径的基础上加载的文件
		require(['echarts', module // 使用柱状图就加载bar模块，按需加载
		],
		function(ec) {
			// 为echarts对象加载数据 
			var myChart = ec.init(document.getElementById(serverLine));
			myChart.setOption(option)
		});
	}
}
