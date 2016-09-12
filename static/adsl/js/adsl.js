/**
 * Created by yzs on 16-9-7.
 */
//根据条目设置宽度

//控制面板侧滑效果
$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("active");
});

function SetHeight(jData) {
    var iLen = 1;
    for (i in  jData['result']['data']) {
        iLen++
    }
    iHeight = iLen * 120;
    document.getElementById("main").style.height = iHeight + "px";
}

//显示数据更新的日期
function showDate(sDate) {
    var sTip = '数据生成于：' + sDate;
    $('#yzs-date').html(sTip);
}

$(function () {
    $('#toggle-traffic').change(function () {
        bSwitchTraffic = $(this).prop('checked');
    })
});

function IsUpdate() {
    if (bSwitchTraffic) {
        return 1
    } else {
        return 0
    }
}

// 基于准备好的dom，初始化echarts实例
function DynamicDrawChart() {
    if (!IsUpdate()) {
        return
    }
    $.ajax({
        // url: '/zabbix/chart/' + sZabbixIP,
        url: '/custom/output/',
        data: "key=adsl",// data: '{ip:' + sZabbixIP + ',line:' + sTagID + '}',
        type: 'GET',
        success: function (sData) {//complete() will always get called no matter if the ajax call was successful or not
            jData = JSON.parse(sData);
            SetHeight(jData);
            if (jData['success'] == 1) {
                drawChart(jData['result']['data'], 'main');
                showDate(jData['result']['date'])
            } else {
                console.log('后端没能给予正确的数据，提示：' + jData['tip']);
            }
        }
    })
}