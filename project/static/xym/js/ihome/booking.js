function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
})


$(document).ready(function(){

    var path = location.search
    id = path.split('=')[1]

    $.get('/house/detail/' + id +'/', function(data){

        if(data.code == '200'){
            var house_booking = template('house_booking', {ohouse:data.house})
            $('.house-info').html(house_booking)
        }
    });

    $('.submit-btn').click(function(){

        var path = location.search
        id = path.split('=')[1]

        var start_date = $('#start-date').val()
        var end_date = $('#end-date').val()
        $.post('/order/', {house_id:id, start_time:start_date, end_time:end_date},
        function(data){
            if(data.code == '200'){
//                跳转到所有订单的页面
                location.href = '/order/order/'
            }
        });

    });

});