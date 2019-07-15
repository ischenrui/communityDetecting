
/*
    vue框架
*/
$(function() {
var login = new Vue({
    el:"#login-page",
	delimiters:['[[', ']]'],
    /*
    * 声明需要的变量
    */
    data : function() {
    return {
//        isLogin:true,
        account:"",
        password:""
        }
    },
    methods: {

        showError:function(error){
        $(".form-error").find("label").html(error);
        $(".form-error").show();
        },
        validate:function(){
            if (this.account==""){
                this.showError("账号不能为空");
                return false;
            }
            if (this.password==""){
                this.showError("密码不能为空");
                return false;
            }
            return true;
        },
        login:function(evt){
            evt.preventDefault();
            if (!this.validate()){
                return ;
            }
            url='/login/check';
            $.ajax({
                url:url,
                type:'POST',
                data:$("#loginForm").serialize(),
                dataType: 'json',
                success:function(data){
                    re=data.success;
                    if (re){
                        window.location = data.obj.url;
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