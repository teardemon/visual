/**
 * Created by yzs on 16-8-8.
 */

//使用滑动按钮的状态为'刷新变量'赋值

//控制面板侧滑效果
$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("active");
});

function GetLength(jEchartData) {
    var i = 0;
    for (sLine in jEchartData) {
        ++i
    }
    return i
}

function SetHeight() {
    var iWidth = $('.yzs-pie').width();
    $('.yzs-pie').height(iWidth);
}
function InitTag(jEchartData) {
    var i = 0;
    var iEachColNum = 6;//每列最大放的饼图数量
    for (sLine in jEchartData) {
        objectDom = document.getElementById(sLine);
        if (objectDom) {
            continue
        }
        if (i % iEachColNum == 0) {
            var iColNum = i / iEachColNum;
            sTag = '<div class="row" id=' + iColNum + '></div>';
            $("#drawChart-area").append(sTag);
        }
        //bootstrap栅格系统，让bootstrap设置宽度.
        var div_new = '<div id="' + sLine + '" class="yzs-pie col-md-2 col-sm-3 col-md-6"></div>';
        $("#" + iColNum).append(div_new);
        ++i;
    }
    SetHeight()
}

function ShowTime(sDate) {
    var sTip = '数据生成于：' + sDate;
    $('#yzs-date').html(sTip)
}

//当按钮被关闭的时候返回不刷新数据的信号
function IsUpdate() {
    if (bSwitchTraffic) {
        return 1
    } else {
        return 0
    }
}


$(function () {
    $('#toggle-traffic').change(function () {
        bSwitchTraffic = $(this).prop('checked');
    })
});

// 异步加载数据
function AjaxDraw() {
    if (!IsUpdate()) {
        return
    }

    //$.get('/static/idc/cache/pie.json').done(function (jData) {  //done在请求成功后执行
    $.ajax({
        url: '/static/idc/cache/pie.json',
        type: 'GET',
        cache: false,//$.get()方法在url地址固定时，会缓存返回结果，导致不可预料的问题。但在火狐下，则不会缓存。
        success: function (jData) {
            //jEchartData = JSON.parse(sEchartData);//如果后端在输出到文本的时候没有转为json格式则需要在前段转换，不可重复转
            jEchartData = jData['data'];
            sDate = jData['date'];
            ShowTime(sDate);
            // jEchartData = Sort(jEchartData);
            InitTag(jEchartData);
            for (sLine in jEchartData) {
                drawChart(jEchartData[sLine], sLine, 3);
            }
        }
    });
}


//<li><a class="btn-floating red" id="yzs-data-button"><i class="material-icons">pause</i></a></li>
// $("#yzs-data-button").on('click', function () {
//     //id为yzs-data-button的子元素i
//     var sButtonStatus = $("#yzs-data-button i").html();
//     if (sButtonStatus == 'pause') {
//         $("#yzs-data-button i").html('play_arrow');
//         $("#yzs-data-button").removeClass('green');
//         $("#yzs-data-button").addClass('red');
//     } else {
//         $("#yzs-data-button i").html('pause');
//         $("#yzs-data-button").removeClass('red');
//         $("#yzs-data-button").addClass('green');
//     }
// });
