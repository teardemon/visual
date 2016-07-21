dataTemplate={
			name:'',//legend 根据这个属性来控制markLine的生效
			type: 'map',
			mapType: 'china',
			data:[],
			markLine : {
				smooth:true,
				effect : {
					show: true,
					scaleSize: 1,
					period: 30,
					color: '#fff',
					shadowBlur: 10
				},
				itemStyle : {
					normal: {
						borderWidth:1,
						lineStyle: {
							type: 'solid',
							shadowBlur: 10
						}
					}
				},
				data : [
				]
			},
}
