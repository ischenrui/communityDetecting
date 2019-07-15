
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
                pageSize: 20,
                totalNum: 0,
                };
              },
        created() {
                  this.getAllList();
                },
		methods: {
			  handleSizeChange: function(val) {
				edit_vue.pageSize = val;
				this.getAllList(edit_vue.curPage, edit_vue.pageSize);
			  },
			  handleCurrentChange: function(val) {
				edit_vue.curPage = val;
				this.getAllList(edit_vue.curPage, edit_vue.pageSize);
			  },
              getAllList: function(curPage, pageSize) { // 获取数据
				curPage=curPage||1;
				pageSize=pageSize||10;

                url='/spider/data';
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
		},
	});

});