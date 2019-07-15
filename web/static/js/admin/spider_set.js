
/*
    vue框架
*/
$(function() {
var spider_set = new Vue({
    el:"#main-content",
	delimiters:['[[', ']]'],
    /*
    * 声明需要的变量
    */
    data : function() {
    return {
        setting: {},
        rate:70,
        }
    },

    methods: {
        showError:function(error){
            $(".form-error").find("label").html(error);
            $(".form-error").show();
        },
        validate:function(data){
            same_delay = data["delay"] == this.setting.DOWNLOAD_DELAY;
            same_max_req = data['max_req'] == this.setting.CONCURRENT_REQUESTS;
            same_proxy =!(data['proxy'] == "on" ^ this.setting.PROXY_ENABLED);
            same_re_req = !(data['re_req'] == "on" ^ this.setting.RE_REQUEST_ENABLED);
            same_cookie = !(data['cookie'] == "on" ^ this.setting.COOKIES_ENABLED);

            if(same_delay && same_max_req && same_proxy && same_re_req && same_cookie){
                this.showError("参数未改变");
                return false;
            }
            return true;
        },
        get_params: function(){
            url = '/spider/params';
            $.ajax({
                url:url,
                type:'POST',
                data:{},
                dataType: 'json',
                success:function(data){
                    re=data.success;
                    if (re){
                        //成功
                        spider_set.setting=data.obj;
                    }else{
                        spider_set.showError(data.msg);

                    }

                 },
                error:function (res) {
                    console.log(res);
                }
               });
        },
        save:function(evt){
            evt.preventDefault();
            val = $("#setForm .form-control").serialize();
            form_data = val.split("&");
            let obj = {};
            obj['delay'] = 0;
            obj['max_req'] = 16;
            obj['proxy'] = "off";
            obj['re_req'] = "off";
            obj['cookie'] = "off";
            for (let i of form_data) {
                key = i.split("=")[0]
                if(key=="delay"||key=="max_req"){
                    obj[key] = Number(i.split("=")[1]);  //对数组每项用=分解开，=前为对象属性名，=后为属性值
                }else{
                    obj[key] = i.split("=")[1];  //对数组每项用=分解开，=前为对象属性名，=后为属性值
                }
            }

            if (!this.validate(obj)){
                return ;
            }
            url='/spider/save';
            $.ajax({
                url:url,
                type:'POST',
                data:obj,
                dataType: 'json',
                success:function(data){
                    re=data.success;
                    if (re){
                        //成功
                        spider_set.setting=data.obj;
                    }else{
                        spider_set.showError(data.msg);
                    }

                 },
                error:function (res) {
                    console.log(res);
                }
               });
         },

    },
    created:function() {
        this.get_params();
    },
    });

});