function logout() {
    $.ajax({
        url:'/user/logout/',
        type:'DELETE',
        dateType:'json',
        success:function(data){
            if(data.code == '200'){
                location.href='/user/login/'
            }
        }
    });
}

$(document).ready(function(){

    $.get('/user/user/', function(data){
        if(data.code == '200'){
            $('#user-mobile').html(data.user.phone);
            $('#user-name').html(data.user.name);
            $('#user-avatar').attr('src', data.user.avatar)
        }
    });

});