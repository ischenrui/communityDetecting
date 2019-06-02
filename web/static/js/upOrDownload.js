/*
* 
*/

// 上传数据功能
var upload_layout = d3.select("#upload-layout");
d3.select("#upload-data")
	.on("click", function() {
		upload_layout.style("display", "block");
	});
var offset_x, offset_y, isdown = false;
upload_layout.select("#upload-top-layout")
	.on("mousedown", function() {
		offset_x = event.pageX - this.parentNode.offsetLeft;
		offset_y = event.pageY - this.parentNode.offsetTop;
		isdown = true;
		d3.select("#svg")
			.on("mousemove.move-upload-layout", function() {
				if (isdown) {
					upload_layout.style("left", d3.event.pageX - offset_x + "px");
					upload_layout.style("top", d3.event.pageY - offset_y + "px");
				}
			})
	})
	.on("mouseup", function() {
		isdown = false;
	})
	.on("mousemove", function() {
		if (isdown) {
			upload_layout.style("left", event.pageX - offset_x + "px");
			upload_layout.style("top", event.pageY - offset_y + "px");
		}
	});
d3.select("#close-button")
	.on("click", function() {
		upload_layout.style("display", "none");
	});
d3.select("#file-close")
	.on("click", function() {
		upload_layout.style("display", "none");
	});
d3.select("#select-file")
	.on("click", function() {
		document.getElementById("file-input").click();
	});
d3.select("#file-input")
	.on("input propertychange", function() {
		d3.select("#file-name").text(this.value);
		d3.select("file-state").text("等待上传");
	})

// 确认上传
d3.select("#upload-button")
    .on("click", function() {
        var form_data = new FormData();
        var file_info = $("#file-input")[0].files[0];
        var algorithm = $("#algorithm-list .active").attr("data-code");
        form_data.append("file", file_info);
        form_data.append("code", algorithm);
        $.ajax({
            url: "upload",
            type: "POST",
            data: form_data,
            async: false,
            contentType: false,
            processData: false,
            success: function(cur_data) {
                console.log(cur_data);
                data = JSON.parse(cur_data);
                updateData(data);
                d3.select("#upload-layout").style("display", "none");
                d3.select("#file-name").text(this.value);
                d3.select("file-state").text("等待上传");
            },
            error: function() {
                alert("数据上传失败！");
            }
        })
    })

// 导出数据
d3.select("#download-data")
    .on("click", downFile);

// 先清洗数据 再下载
function downFile() {
    var temp = JSON.parse(JSON.stringify(data));
    temp.nodes.forEach(function(node) {
        delete node.index;
        delete node.x;
        delete node.y;
        delete node.vx;
        delete node.vy;
        delete node.color;
        delete node.selected;
        delete node.previouslySelected;
    });
    temp.links.forEach(function(link) {
        delete link.index;
        link.source = link.source.id;
        link.target = link.target.id;
    })
    var elementA = document.createElement('a');
    elementA.setAttribute('href', 'data:text/plain;charset=utf-8,' + JSON.stringify(temp, null, 4));
    var time = new Date().getTime();
    elementA.setAttribute('download', 'data_' + time + '.json');
    elementA.style.display = 'none';
    document.body.appendChild(elementA);
    elementA.click();
    document.body.removeChild(elementA);
}

// 导出图片
d3.select("#download-img")
	.on("click", function() {
		saveSvgAsPng(document.getElementById("container"), "networkGraph.png");
	})