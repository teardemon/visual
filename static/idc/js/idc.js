/**
 * Created by yzs on 16-8-8.
 */
function tagAdd(sLine) {
    objectDom = document.getElementById(sLine);
    if (!objectDom) {
        var div_new = '<div id="' + sLine + '" class="yzs-pie"></div>';
        $("#drawChart-area").append(div_new);
    }
}

function ShowTime(sDate) {
    var sTip = '数据生成于：' + sDate;
    $("#yzs-update-time").html(sTip);
}

//当按钮被关闭的时候返回不刷新数据的信号
function IsUpdate() {
    var sButtonStatus = $("#yzs-data-button i").html();
    if (sButtonStatus == 'play_arrow') {
        return 0
    } else {
        return 1
    }
}

// 异步加载数据
function AjaxDraw() {
    if (!IsUpdate()) {
        return
    }

    //done在请求成功后执行
    $.get('/static/idc/cache/pie.json').done(function (jData) {
        //jEchartData = JSON.parse(sEchartData);//如果后端在输出到文本的时候没有转为json格式则需要在前段转换，不可重复转
        jEchartData = jData['data'];
        sDate = jData['date'];
        console.log(sDate);
        ShowTime(sDate);
        for (sServer in jEchartData) {
            for (sLine in jEchartData[sServer]) {
                tagAdd(sLine);
                drawChart(jEchartData[sServer][sLine], sLine, 2);
            }
        }
    });
}

AjaxDraw();
window.setInterval(AjaxDraw, 30000);

//<li><a class="btn-floating red" id="yzs-data-button"><i class="material-icons">pause</i></a></li>
$("#yzs-data-button").on('click', function () {
    //id为yzs-data-button的子元素i
    var sButtonStatus = $("#yzs-data-button i").html();
    if (sButtonStatus == 'pause') {
        $("#yzs-data-button i").html('play_arrow');
        $("#yzs-data-button").removeClass('green');
        $("#yzs-data-button").addClass('red');
    } else {
        $("#yzs-data-button i").html('pause');
        $("#yzs-data-button").removeClass('red');
        $("#yzs-data-button").addClass('green');
    }
});
