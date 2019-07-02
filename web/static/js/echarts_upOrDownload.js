// 上传数据功能
var upload_layout = $("#upload-layout");
$("#upload-data").on("click", function(e) {
    upload_layout.show();
});

$("#close-button").on("click", function() {
    upload_layout.hide();
});
$("#file-close").on("click", function() {
    upload_layout.hide();
});
$("#select-file").on("click", function() {
    document.getElementById("file-input").click();
});
$("#file-input").on("input propertychange", function() {
		$("#file-name").text(this.value);
		$("#file-state").text("等待上传");
	})

// 确认上传
$("#upload-button")
    .on("click", function() {
        if(RUNING){
            return;
        }
        RUNING = true;
        var form_data = new FormData();
        var file_info = $("#file-input")[0].files[0];
        var algorithm = get_algorithm_and_params();

        form_data.append("file", file_info);
        form_data.append("code", JSON.stringify(algorithm));
        $.ajax({
            url: "upload_echarts",
            type: "POST",
            data: form_data,
            async: false,
            contentType: false,
            processData: false,
            success: function(cur_data) {
//              console.log(cur_data);
                data = JSON.parse(cur_data);
                 updateData(data);
                // 关闭上传框
                $("#upload-layout").hide();
                // 清空待上传文件信息
                // $("#file-name").text(this.value);
                $("#file-state").text("上传成功");
            },
            error: function() {
                alert("数据上传失败！");
            },
            finally:function(){
                console.log("finally");
                RUNING = false;
            }
        })
    })

// 导出数据
$("#download-data")
    .on("click", downFile);

// 先清洗数据 再下载
function downFile() {
    
}

// 导出图片
$("#download-img")
	.on("click", function() {
		saveSvgAsPng(document.getElementById("container"), "networkGraph.png");
    })
    
