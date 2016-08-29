/**
 * Created by yzs on 16-8-26.
 */
function GetOption(jDateValue, sTagID) {
    var aYAxis = [];
    var aDownUsed = [];
    var aDownFree = [];
    var aUpUsed = [];
    var aUpFree = [];
    var aSeriesData = {'up': [], 'use': []};
    for (var sIP in jDateValue) {
        for (var sInterface in jDateValue[sIP]) {
            sPurpose = jDateValue[sIP][sInterface]["purpose"];
            /*
             * "down_total": 200,
             "up_total": 35,
             "down_used": 100,
             "up_used": 10,
             * */
            iDownUsedRate = parseFloat((jDateValue[sIP][sInterface]["down_used"] / jDateValue[sIP][sInterface]["down_total"] * 100).toFixed(0));
            iDownFreeRate = 100 - iDownUsedRate;
            iUpUsedRate = parseFloat((jDateValue[sIP][sInterface]["up_used"] / jDateValue[sIP][sInterface]["up_total"] * 100).toFixed(0));
            iUpFreeRate = 100 - iUpUsedRate;
            aDownUsed.push(iDownUsedRate);
            aDownFree.push(iDownFreeRate);
            aUpUsed.push(iUpUsedRate);
            aUpFree.push(iUpFreeRate);
            aYAxis.push(sPurpose); //y坐标的刻度
        }
    }

    jOption = {
        color: ['#77BB77', '#d9d9d9', '#4EA8E4', '#d9d9d9'],
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {data: ['下载已用百分比', '下载未用百分比', '上传已用百分比', '上传未用百分比']},
        xAxis: [{}],
        yAxis: [
            {
                type: 'category',
                axisTick: {show: false},
                data: aYAxis
            }
        ],
        series: [
            {
                name: '下载已用百分比',
                type: 'bar',
                stack: '柱子A',
                label: {
                    normal: {
                        show: true
                    }
                },
                data: aDownUsed
            },
            {
                name: '下载未用百分比',
                type: 'bar',
                stack: '柱子A',
                label: {
                    normal: {
                        show: true
                    }
                },
                data: aDownFree
            },
            {
                name: '上传已用百分比',
                type: 'bar',
                stack: '柱子B',
                label: {
                    normal: {
                        show: true
                    }
                },
                data: aUpUsed
            }
            ,
            {
                name: '上传未用百分比',
                type: 'bar',
                stack: '柱子B',
                label: {
                    normal: {
                        show: true
//                        position: 'left'
                    }
                },
                data: aUpFree
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
function SetEvent(oChart, sTagID) {
    if (!oChart) {
        return
    }
    oChart.on('click', function (jParam) {
        sID = jOption.yAxis[0].data[jParam['dataIndex']];
        for (sIP in jDateValue) {
            for (sInterface in jDateValue[sIP]) {
                if (jDateValue[sIP][sInterface]['purpose'] == sID) {
                    console.log('ip:' + sIP + ' interface:' + sInterface);
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
    SetEvent(oChart, sTagID);
}