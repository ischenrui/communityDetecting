
/*
    vue框架
*/
$(function() {
var base = new Vue({
    el:"#header-app",
	delimiters:['[[', ']]'],
    /*
    * 声明需要的变量
    */

    methods: {

        showError:function(error){
        $(".form-error").find("label").html(error);
        $(".form-error").show();
        },
        logout:function(evt){
            evt.preventDefault();
            url='/login/logout';
            $.ajax({
                url:url,
                type:'POST',
                data:{},
                dataType: 'json',
                success:function(data){
                    re=data.success;
                    if (re){
                        window.location="/login"
                    }else{
                        login.showError(data.msg);
                    }

                 },
                error:function (res) {
                    console.log(res);
                }
               });
         },
    },
    created:function() {},
    });

});