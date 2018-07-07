$(document).ready(function(){
    $.get('/app/refresh/', function (data){
        if(data.code == '200'){
            // $('#user-name').html(data.name);
            $('#foo1').html(data.nick_name);


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



