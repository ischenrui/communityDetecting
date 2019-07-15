
/*
    vue框架
*/
$(function() {
var add_account = new Vue({
    el:"#main-content",
	delimiters:['[[', ']]'],
    /*
    * 声明需要的变量
    */
    data : function() {
    return {
        account:"",
        name:"",
        password:"",
        type:"",
        a_data:[],
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
            if (this.name==""){
                this.showError("姓名不能为空");
                return false;
            }
            if (this.password==""){
                this.showError("密码不能为空");
                return false;
            }
            if (this.type==""){
                this.showError("请选择用户类型");
                return false;
            }
            return true;
        },
        add:function(evt){
            evt.preventDefault();
            add_account.showError("");
            if (!this.validate()){
                return ;
            }
            url='/add/insert';
            $.ajax({
                url:url,
                type:'POST',
                data:$(".form-control").serialize(),
                dataType: 'json',
                success:function(data){
                    re=data.success;
                    if (re){
                        add_account.get_data();
                    }else{
                        add_account.showError(data.msg);
                    }

                 },
                error:function (res) {
                    console.log(res);
                }
               });
         },
        reset:function(evt){
            evt.preventDefault();
            $(".form-control").val("")
            $.ajax({});
        },
        get_data:function(){
            url='/add/data';
            $.ajax({
                url:url,
                type:'POST',
                data:{},
                dataType: 'json',
                success:function(data){
                    re=data.obj;
                    add_account.a_data = re;
                 },
                error:function (res) {
                    console.log("出错");
                }
               });
        }


    },
    created:function() {
        this.get_data();
    },
    });

});