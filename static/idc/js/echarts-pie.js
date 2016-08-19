/**
 * Created by yzs on 16-7-22.
 * 仅仅对数据进行展示，没有额外的处理
 */

function GetLegendData(jDateValue) {
    var aLegendData = new Array();
    for (var sCircle in jDateValue) {
        for (var index in jDateValue[sCircle]) {
            var sName = jDateValue[sCircle][index]['name'];
            aLegendData.push(sName);
        }
    }
    return aLegendData
}

// 格式化数据,同时给数据进行排序
function Format(jDataValue) {
    var aInner = new Array();
    aInner.push({'name': '已用', 'value': jDataValue.inner.used});
    aInner.push({'name': '未用', 'value': jDataValue.inner.total - jDataValue.inner.used});

    // top10的ip占比
    var aOuter = new Array();
    //占比最高的top10总共使用的流量
    for (var sItem in jDataValue.outer) {
        aOuter.push({'name': sItem, 'value': jDataValue.outer[sItem]});
    }

    var jNowData = {
        'inner': aInner,
        'outer': aOuter
    };
    return jNowData
}

// 内环总为深色，外网第一个总和内环同色，其后为第一个同色系的浅色

function GetOption(jDateValue, sTagID, Theme) {

    aFormated = Format(jDateValue);
    //sColorInner = GetColorInner(JDateValue);


    /*染色方法：
     当一个机房没有10个ip的时候显示意义会不正确
     */
    var iRate = jDateValue.inner.used / jDateValue.inner.total;
    //该样式中，外圈的颜色跟随内圈变化
    if (Theme == 1) {
        if (iRate > 0.9) {
            var aOptionColor = ['#CC3333', '#999999', '#CC3333', '#C4573C', '#C4723C', '#DD6D22', '#D5912B', '#EE9611', '#FF9900', '#D5B32B', '#FFCC00', '#EEEE11', '#00CCFF']; //'#FF0000' red
            var bItemStyleShow = true;
        }
        else if (iRate > 0.7) {
            var aOptionColor = ['#CC7033', '#999999', '#CC7033', '#D5912B', '#EE9611', '#FF9900', '#FFCC00', '#D5D52B', '#E6E61A', '#EEEE11', '#FFFF00', '#CCFF00']; //'#FF8C00'chengse
            var bItemStyleShow = false;
        }
        else {
            var aOptionColor = ['#55AA77', '#999999', '#55AA77', '#3CC457', '#72C43C', '#6DDD22', '#B3B34D', '#C4C43C', '#D5D52B', '#B8DD22', '#C2EE11', '#CCFF00', '#00CCFF']; //'#32cd32' green
            var bItemStyleShow = false;
        }
    }
    //该样式中，外圈的颜色是固定的
    //这个渐变也很花'#CC3333', '#DD6D22', '#EE9611', '#D5B32B', '#FFCC00', '#EEEE11', '#6DDD22', '#B8DD22', '#C2EE11', '#CCFF00'
    else if (Theme == 2) {
        if (iRate > 0.9) {
            var aOptionColor = ['#FF0000', '#999999', '#005c99', '#0091f2', '#19a3ff', '#4db8ff', '#66c2ff', '#80ccff', '#99d6ff', '#b3e0ff', '#ccebff', '#e6f5ff', '#e6f5ff']; //'#FF0000' red
            var bItemStyleShow = true;
        }
        else if (iRate > 0.7) {
            var aOptionColor = ['#FF8C00', '#999999', '#005c99', '#0091f2', '#19a3ff', '#4db8ff', '#66c2ff', '#80ccff', '#99d6ff', '#b3e0ff', '#ccebff', '#e6f5ff', '#e6f5ff']; //'#FF8C00'chengse
            var bItemStyleShow = false;
        }
        else {
            var aOptionColor = ['#32cd32', '#999999', '#005c99', '#0091f2', '#19a3ff', '#4db8ff', '#66c2ff', '#80ccff', '#99d6ff', '#b3e0ff', '#ccebff', '#e6f5ff', '#e6f5ff']; //'#32cd32' green
            var bItemStyleShow = false;
        }
    }
    else {
        if (iRate > 0.9) {
            var aOptionColor = ['#FF0000', '#999999', '#a60000', '#cc0000', '#ff0000', '#e62222', '#e63939', '#e65050', '#e66767', '#e67e7e', '#e69595', '#e6acac']; //'#FF0000' red
            var bItemStyleShow = true;
        }
        else if (iRate > 0.7) {
            var aOptionColor = ['#FF8C00', '#999999', '#a66300', '#cc7a00', '#ff9900', '#ffa319', '#ffad33', '#ffb84d', '#ffc266', '#ffcc80', '#ffd699', '#ffe0b3']; //'#FF8C00'chengse
            var bItemStyleShow = false;
        }
        else {
            var aOptionColor = ['#32cd32', '#999999', '#005900', '#008000', '#00a600', '#00a600', '#00d900', '#5ccc5c', '#70cc70', '#85cc85', '#99cc99', '#adccad']; //'#32cd32' green
            var bItemStyleShow = false;
        }
    }


    var jOption = {
        //颜色按顺时针顺序，由内环到外环取。顺序：已用-未用
        color: aOptionColor,
        tooltip: {//提示框，当聚焦后显示
            trigger: 'item',//触发方式：数据项图形触发
            formatter: "{b}: {c} m/s \<br/\>占比: {d} %"
        },
        title: {
            itemGap: 6,//主副标题之间的间距
            target: 'blank',//打开标题超链接
            text: sTagID,
            //显示未用，以检查计算错误
            subtext: '总带宽: ' + jDateValue.inner.total + 'Mb/s\n' + '已用: ' + jDateValue.inner.used + 'M/s',//\n'+'未用:'+non_used+ 'M/s',
            x: 'center',
            textStyle: {
                fontSize: 32
            }
        },
        // animation: false, 关闭动画效果，关闭对页面奔溃的改善不大
        /* 工具栏
         * legend: {
         orient: 'vertical',
         x: 'left',
         data: aLegendData
         },
         * */
        series: [
            {//内环的样式
                name: jDateValue.outer_name,
                center: ['50%', '63%'],//图形的中心坐标，默认['50%'，‘50%’]
                type: 'pie',
                radius: [0, '60%'], //内环的大小，内径为0则为圆

                label: {
                    normal: {
                        position: 'inner'
                    }
                },
                data: aFormated['inner'],
                itemStyle: {
                    normal: {
                        label: {
                            show: true,
                            position: 'inner',
                            formatter: "{b}\n{d}%" //当不聚焦在图形上时,显示的格式，不设置的话会挡住副标题
                        }
                    }
                }
            },
            {//外环的样式
                name: '外环为Top流量',
                center: ['50%', '63%'],//图形的中心坐标，默认['50%'，‘50%’]
                type: 'pie',
                radius: ['67%', '74%'],//外环的内径和外径
                data: aFormated['outer'],
                itemStyle: {
                    normal: { //没有聚焦时的样式
                        label: {
                            show: false //ItemStyleShow //因为溢出div的设置还不会做，所以暂时用false
                        },
                        labelLine: {
                            show: bItemStyleShow //
                        }
                    },
                    emphasis: { //聚焦以后的样式
                        label: {
                            show: false //因为溢出div的设置还不会做，所以暂时用false
                        },
                        labelLine: {
                            show: true
                        }
                    }
                }
            }
        ]
    };
    return jOption
}

function SetOption(jOption, sTagID) {
    objectDom = document.getElementById(sTagID);
    if (objectDom) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(objectDom);
    } else {
        alert('dom还没有加载！');
    }
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(jOption);
    return myChart
}

function SetEvent(oChart) {
    if (!oChart) {
        return
    }
    oChart.on('click', function (param) {
        //     用于弹出 数据
        console.log(param.seriesName);
        //name 用于弹出 数据
        console.log(param.name);
    })
}

function drawChart(jDateValue, sTagID, Theme) {
    jOption = GetOption(jDateValue, sTagID, Theme);
    oChart = SetOption(jOption, sTagID);
    SetEvent(oChart)
}
