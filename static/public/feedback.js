/**
 * Created by yzs on 16-9-19.
 */
//on() 方法在被选元素及子元素上添加一个或多个事件处理程序。
$(".icon-exclamation-sign").on("click", function () {
    $("#yzs-model-feedback").modal('show');
});

$("#yzs-feedback-submit").on("click", function () {
    $("#yzs-model-feedback").modal('hide');
    var sFeedback = $("#yzs-textarea").val(); //用户反馈的信息
    if (sFeedback) {
        var sFeedback = "【数据可视化用户反馈】" + sFeedback;
    } else {
        return null
    }
    $.ajax({
        url: '/api/alert',
        data: "content=" + sFeedback + "&number=8766,6505   ",// data: '{ip:' + sZabbixIP + ',line:' + sTagID + '}',
        type: 'GET',
        success: function (jData) {
            //清除已填写信息
            $("#yzs-textarea").val('');
            ohSnap('反馈已送达，谢谢~~', {'color': 'blue'}, 15000)
        }
    });
});