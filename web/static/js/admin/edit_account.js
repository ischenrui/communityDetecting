
/*
    vue框架
*/
$(function() {
	var edit_vue = new Vue({
		el:"#main-content",
		delimiters:['[[', ']]'],
		data() {
                return{
                result: [],
                currentPage: 1,
                pageSize: 10,
                totalNum: 0,
                the_account: {}
                };
              },
        created() {
                  this.getAllList();
                },
		methods: {
			  handleSizeChange: function(val) {
				console.log(`每页 ${val} 条`);
				edit_vue.pageSize = val;
				this.getAllList(edit_vue.curPage, edit_vue.pageSize);
			  },
			  handleCurrentChange: function(val) {
				console.log(`当前页: ${val}`);
				edit_vue.curPage = val;
				this.getAllList(edit_vue.curPage, edit_vue.pageSize);
			  },
              getAllList: function(curPage, pageSize) { // 获取数据
				curPage=curPage||1;
				pageSize=pageSize||10;

                url='/accounts/list';
                var params= {};
                params['curPage'] = curPage;
                params['pageSize'] = pageSize;
                var data= {
                    data: JSON.stringify(params),
                };
                $.ajax({
                    url:url,
                    type:'POST',
                    data:data,
                    dataType: 'json',
                    success:function(data){
                        re=data.obj;
                        edit_vue.result = re.data;
                        edit_vue.totalNum = re.total;
                    },
                    error:function (res) {
                        console.log(`error`);
                    }
                });
            },
              remove: function(_id) { // 获取数据
				console.log(_id);

                url='/accounts/delete';
                var params= {};
                params['id'] = _id;
                var data= {
                    data: JSON.stringify(params),
                };
                $.ajax({
                    url:url,
                    type:'POST',
                    data:data,
                    dataType: 'json',
                    success:function(data){
                        console.log("成功");
                        edit_vue.getAllList(edit_vue.currentPage, edit_vue.pageSize);
                    },
                    error:function (res) {
                        console.log(`error`);
                    }
                });
            },
              edit: function(item) {
                console.log(item.id)
                edit_vue.the_account = item
                // 显示编辑区域
                var edit_block = document.getElementById("edit_block");
                edit_block.style.display = "inline";
              },
              showError: function(error) {
                $(".form-error").find("label").html(error);
                $(".form-error").show();
              },
              update_submit: function(evt) {
                evt.preventDefault();
                val = $(".form-control").serialize();
                form_data = val.split("&");
                let obj = {};
                for (let i of form_data) {
                  obj[i.split("=")[0]] = i.split("=")[1];  //对数组每项用=分解开，=前为对象属性名，=后为属性值
                }
                if(obj["name"]==""){
                    obj['name'] = edit_vue.the_account["name"];
                }
                if(obj["password"]==""){
                    obj['password'] = edit_vue.the_account["psd"];
                }
                if(obj["type"]==""){
                    obj['type'] = edit_vue.the_account["status"];
                }
                obj["id"] = edit_vue.the_account["id"];

                url = '/accounts/update'
                $.ajax({
                    url:url,
                    type:'POST',
                    data: obj,
                    dataType: 'json',
                    success:function(data){
                        re=data.success;
                        if(re){
                            console.log("更新成功");
                            edit_vue.getAllList(edit_vue.currentPage, edit_vue.pageSize);
                            edit_vue.the_account = {};
                            // 隐藏编辑区域
                            var edit_block = document.getElementById("edit_block");
                            edit_block.style.display = "none";
                        }else{
                            console.log(data.msg);
                        }
                    },
                    error:function (res) {
                        console.log(`error`);
                    }
                });
              },
              clear: function(evt) {
                console.log("clear**************")
                $(".form-control").val("");
                $.ajax({});
              },
		},
	});

});