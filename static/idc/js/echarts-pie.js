/**
 * Created by yzs on 16-7-22.
 * 仅仅对数据进行展示，没有额外的处理
 */

function GetLegendData(jDataValue) {
    var aLegendData = new Array();
    for (var sCircle in jDataValue) {
        for (var index in jDataValue[sCircle]) {
            var sName = jDataValue[sCircle][index]['name'];
            aLegendData.push(sName);
        }
    }
    return aLegendData
}

function FormatSeriesName(jDataValue) {
    var sIP = jDataValue.inner_name;
    var sName = '已用:' + iUsed + ' Mb/s<br/>未用:' + iFree + ' Mb/s<br/>IP:' + sIP;
    return sName
}

function FormatInner(jDataValue) {
    var aInner = new Array();
    iUsed = jDataValue.inner.used.toFixed(2);
    // var sName = '带宽:' + iUsed + ' Mb/s<br/>IP:' + sIP + '<br/>占机房已用带宽百分比:';
    aInner.push({'name': '', 'value': iUsed});

    iFree = (jDataValue.inner.total - jDataValue.inner.used).toFixed(2);
    // var sName = '带宽:' + iFree + ' Mb/s<br/>IP:' + sIP + '<br/>占机房已用带宽百分比:';
    aInner.push({'name': '', 'value': iFree});
    return aInner
}

function FormatOuter(jDataValue) {
    // top10的ip占比
    var aOuter = new Array();
    //占比最高的top10总共使用的流量
    for (var sIP in jDataValue.outer) {
        //用途:<br/>
        fValue = jDataValue.outer[sIP]['traffic'];
        sUsage = jDataValue.outer[sIP]['usage'];
        sUser = jDataValue.outer[sIP]['user'];
        fValue = fValue.toFixed(2);//iValue必须是非０浮点数
        fPercent = (fValue / jDataValue.used * 100).toFixed(2);
        sName = '用途:' + sUsage + '<br/>使用人:' + sUser + '<br/>带宽:' + fValue + ' Mb/s<br/>IP:' + sIP + '<br/>占机房已用带宽百分比:' + fPercent + ' %';
        aOuter.push({'name': sName, 'value': fValue});
    }
    return aOuter
}

// 格式化数据,同时给数据进行排序
function Format(jDataValue) {
    aInner = FormatInner(jDataValue);
    aOuter = FormatOuter(jDataValue);
    sSeriesName = FormatSeriesName(jDataValue);
    var jNowData = {
        'inner': aInner,
        'outer': aOuter,
        'name': sSeriesName
    };
    return jNowData
}

// 内环总为深色，外网第一个总和内环同色，其后为第一个同色系的浅色

function GetOption(jDataValue, sTagID, Theme) {
    if (!jDataValue) {
        console.log('jDataValue为空');
    }
    aFormated = Format(jDataValue);
    //sColorInner = GetColorInner(jDataValue);


    /*染色方法：
     当一个机房没有10个ip的时候显示意义会不正确
     */
    var iRate = jDataValue.inner.used / jDataValue.inner.total;
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
    //该样式中，外圈的颜色是固定的。内圈颜色保持红黄绿随机房线路百分比变换
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
    else if (Theme == 3) {
        //该样式是波哥要求的：外环染色:分档４档染色。<=50 , 500-100 , 100-200,200>=
        if (iRate > 0.9) {
            var aOptionColor = ['#FF0000', '#999999']; //'#FF0000' red
            var bItemStyleShow = true;
        }
        else if (iRate > 0.7) {
            var aOptionColor = ['#FF8C00', '#999999']; //'#FF8C00'chengse
            var bItemStyleShow = false;
        }
        else {
            var aOptionColor = ['#32cd32', '#999999']; //'#32cd32' green
            var bItemStyleShow = false;
        }
        for (i in aFormated.outer) {
            aItem = aFormated.outer[i]; //{‘name’:'vaule'}
            if (aItem['value'] >= 200) {
                aOptionColor.push('#005c99');
            } else if (100 <= aItem['value'] && aItem['value'] < 200) {
                aOptionColor.push('#19a3ff');
            } else if (50 <= aItem['value'] && aItem['value'] < 100) {
                aOptionColor.push('#b3e0ff');
            } else {
                aOptionColor.push('#e6f5ff');
            }
        }
    } else {
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
            /*
             饼图、仪表盘、漏斗图: {a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
             {a} series.name
             {b} 根据{'name': '已用', 'value': jDataValue.inner.used} 中的name决定
             {c} {'name': '已用', 'value': jDataValue.inner.used} 中的value决定
             {d}

             外环没有{a} 即:外环没有系列名称
             内环没有{b} 即:项目名，数据格式为 {'':值}
             * */
            formatter: "{a} {b}"
        },
        title: {
            itemGap: 6,//主副标题之间的间距
            target: 'blank',//打开标题超链接
            text: sTagID,
            //显示未用，以检查计算错误
            subtext: '总带宽: ' + jDataValue.inner.total + ' Mb/s\n' + '已用: ' + jDataValue.inner.used + ' Mb/s',//\n'+'未用:'+non_used+ 'M/s',
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
                name: aFormated.name,
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
                name: '',
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


function GetImgTag(jData) {
    if (!jData) {
        return ''
    }
    jData = JSON.parse(jData);
    sOneDay = jData['traffic']['1day'];
    sSevenDay = jData['traffic']['7day'];
    sOneDay = '<center><strong><h3>1 day</h3></center></strong><img src="' + sOneDay + '"></img>';
    sSevenDay = '<center><strong><h3>7 day</h3></center></strong><img src="' + sSevenDay + '"></img>';
    sTag = sOneDay + sSevenDay;
    return sTag
}

function InsertModel(sTag) {
    $(".modal-body").html(sTag);
}

function ShownModel() {
    $("#myModal").modal('show');
}

function ZabbixChart(sTip, sTagID) {
    //sTip为图像聚焦时显示的提示框文本
    //外环类似为：用途:CDN下载<br/>带宽:336.95 Mb/s<br/>IP:113.106.204.141<br/>占机房已用带宽百分比: 惠州电信2
    //内环类似为:
    var re = /\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}/g;
    sTip = sTip.match(re);
    console.log(sTip, sTagID);
    $.ajax({
        // url: '/zabbix/chart/' + sZabbixIP,
        url: '/zabbix/chart',
        data: "ip=" + sTip + "&line=" + sTagID,// data: '{ip:' + sZabbixIP + ',line:' + sTagID + '}',
        type: 'GET',
        success: function (jData) {
            sTag = GetImgTag(jData);
            InsertModel(sTag);
            ShownModel();
        }
    });
}

function SetEvent(oChart, sTagID) {
    if (!oChart) {
        return
    }
    oChart.on('click', function (param) {
        if (param.name == 'other') {
            //用户当前点击的是外环的'other',外环显示机房top10和other流量，other是不需要弹框显示的
            return ''
        }
        // 用于弹出 数据
        sOuterName = jOption.series[1].name;
        if (param.seriesName == sOuterName) {
            //用户当前点击的是外环
            var sTip = param.name; //{'ip':'值'}
        } else {
            //用户当前点击的是内环
            var sTip = param.seriesName
        }
        ZabbixChart(sTip, sTagID)
    })
}

/*
 * jDataValue：用于画图的数据
 * sTagID：画图的html标签的id
 * Theme：绘图的样式编号
 * */
function drawChart(jDataValue, sTagID, Theme) {
    jOption = GetOption(jDataValue, sTagID, Theme);
    oChart = SetOption(jOption, sTagID);
    SetEvent(oChart, sTagID);
}
