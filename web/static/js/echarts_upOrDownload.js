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
            alert("请不要重复提交~");
            return;
        }
        RUNING = true;
        var form_data = new FormData();
        var file_info = $("#file-input")[0].files[0];
        
        var file_name = getFileName($("#file-input").val())
               
        var algorithm = get_algorithm_and_params();

        form_data.append("file", file_info);
        form_data.append("code", JSON.stringify(algorithm));
        myChart.showLoading();
        $.ajax({
            url: "upload_echarts",
            type: "POST",
            data: form_data,
            async: false,
            contentType: false,
            processData: false,
            success: function(cur_data) {
                sessionStorage.setItem("data", cur_data);
                sessionStorage.setItem("filename", file_name);

                // console.log(cur_data);
                data = JSON.parse(cur_data);
                // console.log(data);
                format_data_to_echarts(data);
                updateData(data);
                // 关闭上传框
                $("#upload-layout").hide();
                // 清空待上传文件信息
                // $("#file-name").text(this.value);
                $("#file-state").text("上传成功");
                RUNING = false;
            },
            error: function() {
                alert("数据上传失败！");
                RUNING = false;
            },
            finally:function(){
                console.log("finally");
            }
        })
    })

// 导出数据
$("#download-data")
    .on("click", downFile);

// 下载数据
function downFile() {
    let file_name = sessionStorage.getItem("filename");
    if(file_name){
        file_name += ".json";
        let data = sessionStorage.getItem("data");

        let file = new File([data], file_name, { type: "text/plain;charset=utf-8" });
        saveAs(file);
    }
}

// 导出图片
$("#download-img")
	.on("click", function() {
		saveSvgAsPng(document.getElementById("container"), "networkGraph.png");
    })
    
/**
 * 将文件名从文件路径中分离
 * @param {string} file_path 
 */
function getFileName(file_path){
    /**
     * "C:\fakepath\北京大学工学院.gml"
     * ==>  ["C:\fakepath\北京大学工学院", "gml"]
     * ==>  ["C:","fakepath","北京大学工学院"]
     */
    let path_arr = file_path.split(".")[0].split("\\");
    return path_arr[path_arr.length -1]
}