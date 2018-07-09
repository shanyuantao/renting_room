$(document).ready(function(){
    $.get('/app/refresh/', function (data){
        if(data.code == '200'){
            str1= '<img height="38" width="38" src="'+ data.avatar + '" alt="读取头像失败QAQ">';
            str2 = '<span color="pink">' + data.nick_name + '</span>';
            str3 = str1 + str2;

            $('#for_avatar').html(str3)
            // $("#for_avatar").html();dsadsa
            // $('#foo1').html(data.nick_name);
        }else{
            str4 = '<ul><li><audio src="http://dx.sc.chinaz.com/Files/DownLoad/sound1/201211/2296.mp3" id="audio1" hidden="true" autoplay="true" loop="true"></audio></li><li color="red" >异常进入,开始启动联网警报!!!</li>\n' +
                '<li id="for_avatar"><img height="38" width="38" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1531056190164&di=4f03ab19ee508f5da71a3674ae77c926&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20180313%2F4c9c1072f3354e389672120f7040e176.gif" alt=""> <span id="foo1"></span></li>\n' +
                '</ul>';
            $('.navigation').html(str4)
        }


    })
});

function update_pwd(){
    password = $('#password').val();
    password1= $('#password1').val();
    password2 = $('#password2').val();
    $.ajax({
        url:'/app/update_pwd/',
        type:'POST',
        dataType:'json',
        data:{'password':password,
        'password1':password1,
        'password2':password2},
        success:function(data){
            if(data.code==200){
                alert(data.msg);
                location.href='/app/hello/'
            }else{
                alert(data.msg);

            }
        },
        error:function (data) {
            alert(data.msg)
        }
    })
}

function search(){
    to_page = $('#jumpNumTxt').val().trim();
    total_page = $('#foo2').val();
    var re = /^[1-9]+.?[0-9]*/;//判断正整数/[1−9]+[0−9]∗]∗/
    if(!re.test(to_page)){
        alert('请输入大于0的整数')
    }else if(parseInt(to_page) > parseInt(total_page)){
        alert('页码必须小于总页数')
    }else{
        location.href='/app/house_manage/' + to_page + '/'
    }
}

function select_search(){
    area_id = $('#fyXq').val();
    price_range = $('#fyDh').val();
    acreage_range= $('#fyHx').val();
    house_type = $('#fyStatus').val();
    location.href = '/app/search/'+ area_id + '/'+ price_range + '/'+ acreage_range + '/'+ house_type + '/' + '1' + '/'
    /*
    $.ajax({
        type:'POST',
        data: {
            'area_id':area_id,
            'price_range':price_range,
            'acreage_range':acreage_range,
            'house_type':house_type
        },
        url: '/app/search/',
        dataTYpe: 'json',
        success:function (data) {
            alert('写错了')
        }
    })*/

}


