/**
 * Created by yzs on 16-8-26.
 */
function Rate(jDateValue) {
    var aYAxis = [];
    var aDownUsed = [];
    var aDownFree = [];
    var aUpUsed = [];
    var aUpFree = [];

    for (var sIP in jDateValue) {
        for (var sInterface in jDateValue[sIP]) {
            sPurpose = jDateValue[sIP][sInterface]["purpose"];
            iDownUsedRate = parseFloat((jDateValue[sIP][sInterface]["down_used"] / jDateValue[sIP][sInterface]["down_total"] * 100).toFixed(0));
            iDownFreeRate = 100 - iDownUsedRate;
            if (iDownFreeRate < 0) {
                iDownFreeRate = 0;
                //此处需要增加报警
            }
            iUpUsedRate = parseFloat((jDateValue[sIP][sInterface]["up_used"] / jDateValue[sIP][sInterface]["up_total"] * 100).toFixed(0));
            iUpFreeRate = 100 - iUpUsedRate;
            if (iUpFreeRate < 0) {
                iUpFreeRate = 0;
                //此处需要增加报警
            }
            aDownUsed.push(iDownUsedRate);
            aDownFree.push(iDownFreeRate);
            aUpUsed.push(iUpUsedRate);
            aUpFree.push(iUpFreeRate);
            aYAxis.push(sPurpose); //y坐标的刻度
        }
    }
    var aParaOption = {
        'down_used': aDownUsed,
        'down_free': aDownFree,
        'up_used': aUpUsed,
        'up_free': aUpFree,
        'yaxis': aYAxis
    };
    return aParaOption
}

function Value(jDateValue) {
    var aYAxis = [];
    var aDownUsed = [];
    var aDownFree = [];
    var aUpUsed = [];
    var aUpFree = [];

    for (var sIP in jDateValue) {
        for (var sInterface in jDateValue[sIP]) {
            sPurpose = jDateValue[sIP][sInterface]["purpose"];

            iDownUsed = parseFloat(jDateValue[sIP][sInterface]["down_used"]).toFixed(0);
            iDownFree = parseFloat(jDateValue[sIP][sInterface]["down_total"] - iDownUsed).toFixed(0);

            iUpUsed = parseFloat(jDateValue[sIP][sInterface]["up_used"]).toFixed(0);
            iUpFree = parseFloat(jDateValue[sIP][sInterface]["up_total"] - iUpUsed).toFixed(0);

            aDownUsed.push(iDownUsed);
            aDownFree.push(iDownFree);
            aUpUsed.push(iUpUsed);
            aUpFree.push(iUpFree);
            aYAxis.push(sPurpose); //y坐标的刻度
        }
    }
    var aParaOption = {
        'down_used': aDownUsed,
        'down_free': aDownFree,
        'up_used': aUpUsed,
        'up_free': aUpFree,
        'yaxis': aYAxis
    };
    return aParaOption
}

function GetOption(jDateValue, sTagID) {
    // var aParaOption = Rate(jDateValue);
    var aParaOption = Value(jDateValue);
    jOption = {
        color: ['#77BB77', '#d9d9d9', '#4EA8E4', '#d9d9d9'],
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {data: ['下载已用', '下载未用', '上传已用', '上传未用']},
        xAxis: [{}],
        yAxis: [
            {
                type: 'category',
                axisTick: {show: false},
                data: aParaOption['yaxis']
            }
        ],
        series: [
            {
                name: '下载已用',
                type: 'bar',
                stack: '柱子A',
                label: {
                    normal: {
                        show: true
                    }
                },
                data: aParaOption['down_used']
            },
            {
                name: '下载未用',
                type: 'bar',
                stack: '柱子A',
                label: {
                    normal: {
                        show: true
                    }
                },
                data: aParaOption['down_free']
            },
            {
                name: '上传已用',
                type: 'bar',
                stack: '柱子B',
                label: {
                    normal: {
                        show: true
                    }
                },
                data: aParaOption['up_used']
            }
            ,
            {
                name: '上传未用',
                type: 'bar',
                stack: '柱子B',
                label: {
                    normal: {
                        show: true
//                        position: 'left'
                    }
                },
                data: aParaOption['up_free']
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

function ZabbixChart(sZabbixIP, sTagID) {
    $.ajax({
        // url: '/zabbix/chart/' + sZabbixIP,
        url: '/zabbix/chart',
        data: "ip=" + sZabbixIP + "&line=" + sTagID,// data: '{ip:' + sZabbixIP + ',line:' + sTagID + '}',
        type: 'GET',
        success: function (jData) {
            sTag = GetImgTag(jData);
            InsertModel(sTag);
            ShownModel();
        }
    });
}

function InsertModel(sTag) {
    $(".modal-body").html(sTag);
}

function ShownModel() {
    $("#myModal").modal('show');
}

function ZabbixChart(sIP, sInterface='', sTagID='') {
    //sTip为图像聚焦时显示的提示框文本
    //外环类似为：用途:CDN下载<br/>带宽:336.95 Mb/s<br/>IP:113.106.204.141<br/>占机房已用带宽百分比: 惠州电信2
    //内环类似为:
    var re = /\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}/g;
    sIP = sIP.match(re);
    console.log(sIP, sInterface);
    $.ajax({
        // url: '/zabbix/chart/' + sZabbixIP,
        url: '/zabbix/chart',
        data: "ip=" + sIP + "&interface=" + sInterface,// data: '{ip:' + sZabbixIP + ',line:' + sTagID + '}',
        type: 'GET',
        success: function (jData) {
            sTag = GetImgTag(jData);
            InsertModel(sTag);
            ShownModel();
        }
    });
}

function SetEvent(oChart, jDateValue) {
    if (!oChart) {
        return
    }
    oChart.on('click', function (jParam) {
        sID = jOption.yAxis[0].data[jParam['dataIndex']];
        for (sIP in jDateValue) {
            for (sInterface in jDateValue[sIP]) {
                if (jDateValue[sIP][sInterface]['purpose'] == sID) {
                    ZabbixChart(sIP, sInterface);
                    //下一步根据graph id绘制图形
                }
            }
        }
    })
}
// 使用刚指定的配置项和数据显示图表。
function drawChart(jDateValue, sTagID) {
    var jOption = GetOption(jDateValue, sTagID);
    var oChart = SetOption(jOption, sTagID);
    SetEvent(oChart, jDateValue);
}