/*
* 
*/

var SHOWCONFIG = {
    "screen": false,
    "brush": false,
    "info": true,
    "setting": false,
    "route": false,
    "bar_chart": false,
    "node_text": true,
    "link_text": false,
    "marker": true,
    "result" : false,
    "algorithm": true
};

// 算法显示开关
d3.select("#algorithm-show")
    .on("click", function(){
        d3.select(this).classed("active", SHOWCONFIG.algorithm = !SHOWCONFIG.algorithm);
        d3.select("#angle-right").style("animation", SHOWCONFIG.algorithm === true ? "angle-down 1s forwards" : "angle-right 1s forwards")
        
    });
// 算法选择
d3.select("#algorithm-list")
    .on("click", function(){
        console.log(this);
        let event = d3.event,
            target = event.srcElement;
        d3.selectAll("#algorithm-list .active").classed("active", false);
        d3.select(target).classed("active", true);
        //阻止事件向上冒泡
        event.stopPropagation();
    });

// 信息显示开关
d3.select("#info-show")
    .on("click", function() {
        d3.select(this).classed("active", SHOWCONFIG.info = !SHOWCONFIG.info);
        d3.select("#info-layout").style("animation", SHOWCONFIG.info === true ? "show-info 1s forwards" : "hide-info 1s forwards");
    });


// 柱状图显示开关
d3.select("#bar-graph-show")
    .on("click", function () {
        d3.select(this).classed("active", SHOWCONFIG.bar_chart = !SHOWCONFIG.bar_chart);
        d3.select("#bar-graph")
            .attr("transform", "translate(" + (window.innerWidth - BARCONFIG.width + 2) + ", " + 32 + ")")
        if (SHOWCONFIG.bar_chart === true) {
            bar_graph.style("animation", "show-bar-chart 1s forwards");
        }
        else {
            bar_graph.style("animation", "hide-bar-chart 1s forwards");
        }
    });

// 节点标签显示开关
d3.select("#node-button").on("click", function() {
        d3.select(this).classed("active", SHOWCONFIG.node_text = !SHOWCONFIG.node_text);
        node_layout.selectAll("text").style("display", SHOWCONFIG.node_text === true ? "block" : "none");
    });

// 关系标签显示开关
d3.select("#link-button")
    .on("click", function() {
        d3.select(this).classed("active", SHOWCONFIG.link_text = !SHOWCONFIG.link_text);
        text_layout.selectAll("text").style("display", SHOWCONFIG.link_text === true ? "block" : "none");
    });

// 箭头显示开关
d3.select("#marker-button")
    .on("click", function() {
        d3.select(this).classed("active", SHOWCONFIG.marker = !SHOWCONFIG.marker);
        network_graph.select("marker")
            .select("path")
            .style("display", SHOWCONFIG.marker === true ? "block" : "none");
    });


// 分析结果显示开关
var result_box = d3.select("#result-box");
d3.select("#result-button")
    .on("click", function() {
        d3.select(this).classed("active", SHOWCONFIG.result = !SHOWCONFIG.result);
        result_box.style("animation", SHOWCONFIG.result === true ? "show-box 1s forwards" : "hide-box 1s forwards");
    });



// 设置面板显示开关
var setting_box = d3.select("#setting-box");
d3.selectAll("#setting-visiable-button")
    .on("click", function() {
        if (SHOWCONFIG.route === true) {
            SHOWCONFIG.route = false;
            route_box.style("animation", "hide-box 1s forwards");
        }
        SHOWCONFIG.setting = !SHOWCONFIG.setting;
        setting_box.style("animation", SHOWCONFIG.setting === true ? "show-box 1s forwards" : "hide-box 1s forwards");
    });

// 路径查找显示开关
var route_box = d3.select("#route-box");
d3.select("#route-visiable-button")
    .on("click", function() {
        if (SHOWCONFIG.setting === true) {
            SHOWCONFIG.setting = false;
            setting_box.style("animation", "hide-box 1s forwards");
        }
        SHOWCONFIG.route = !SHOWCONFIG.route;
        route_box.style("animation", SHOWCONFIG.route === true ? "show-box 1s forwards" : "hide-box 1s forwards");
    });


// 全屏切换
d3.select("#screen-button")
    .on("click", function() {
        SHOWCONFIG.screen = !SHOWCONFIG.screen;
        SHOWCONFIG.screen === true ? enterFullScreen() : exitFullScreen();
        d3.select("#screen-switch")
            .attr("class", SHOWCONFIG.screen === true ? "fa fa-compress" : "fa fa-expand");
    });

// shift 点击切换框选
document.onkeydown = function(ev) {
    var e = ev || window.ev || arguments.callee.caller.arguments[0];
    if(e && e.keyCode === 16){
        SHOWCONFIG.brush = !SHOWCONFIG.brush;
        brush_svg.style("display", SHOWCONFIG.brush === true ? "block" : "none");
    }
};

//进入全屏
function enterFullScreen() {
    var de = document.documentElement;
    if (de.requestFullscreen) {
        de.requestFullscreen();
    } else if (de.mozRequestFullScreen) {
        de.mozRequestFullScreen();
    } else if (de.webkitRequestFullScreen) {
        de.webkitRequestFullScreen();
    }
}

//退出全屏
function exitFullScreen() {
    var de = document;
    if (de.exitFullscreen) {
        de.exitFullscreen();
    } else if (de.mozCancelFullScreen) {
        de.mozCancelFullScreen();
    } else if (de.webkitCancelFullScreen) {
        de.webkitCancelFullScreen();
    }
}