var myChart = echarts.init(document.getElementById('container'));

var SCHOOL_LIST = {}

graph_option = {
    tooltip: {
        formatter: function (params) {
            if (params.dataType == "node") {
                //设置提示框的内容和格式 节点和边都显示name属性
                return `<strong>节点属性</strong><hr>姓名：${params.data.label}</b><br>所属学校：${params.data.school}<br>所属学院：${params.data.insititution}`;
            }
            else{
                return `<strong>关系属性</strong><hr>
                论文合作：${params.data.paper}次<br>专利合作：${params.data.patent}次<br>项目合作：${params.data.project}次<br>`;
            }
        }
    },
    toolbox: {
        　　show: true,
        　　feature: {
        　　　　saveAsImage: {
                    show:true, 
                    // excludeComponents :['toolbox'],
                    type:"png",
                    pixelRatio: 2
        　　　　}
        　　}
    },
    // 图例
    legend: [{
        // selectedMode: 'single',
        data: undefined
    }],
    animation: true,
    series : [
        {
            type: 'graph',
            layout: 'force',
            data: undefined,
            links: undefined,
            categories: undefined,

            // // 边的长度范围
            // edgeLength: [10, 50],

            //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            roam: true,

            // 当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
            focusNodeAdjacency:true,
            // 是否启用图例 hover(悬停) 时的联动高亮。
            legendHoverLink : true,

            label: {
                normal: {
                    position: 'inside',
                    show : true,

                    //回调函数，显示用户名
                    formatter: function(params){
                        return params.data.label;
                    }
                }
            },
            force: {
                repulsion : [10,100],//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                gravity : 0.1,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                edgeLength :[10,80],//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
                layoutAnimation : true
            },

            lineStyle: {
                show : true,
                color: 'target',//决定边的颜色是与起点相同还是与终点相同
                curveness: 0.1//边的曲度，支持从 0 到 1 的值，值越大曲度越大。
            }
        }
    ]
}

function reload_graph(data){
    if(!"nodes" in data) return;
    let nodes = data.nodes, links = data.links, cates = data.community;
    // console.log(nodes.length, links.length, cates.length);
    graph_option.series[0].data = nodes;
    graph_option.series[0].links = links;

    // 设置保存为图片时的名称
    graph_option.toolbox.feature.name = sessionStorage.getItem("filename");

    let categories = [];
    for (var i = 0; i < cates.length; i++) {
        categories[i] = {
            name: '社区' + (i + 1)
        };
    }
    graph_option.series[0].categories = categories;
    graph_option.legend = [{
        data: categories.map(function (a) {
            return a.name;
        })
    }],
    myChart.setOption(graph_option);
    myChart.hideLoading();
}

$("#select-college").change(function(){
    let school = $(this).children("option:selected").text();
    //
    if(school in SCHOOL_LIST){
        setInstitution(SCHOOL_LIST[school],school);
    }
    else{
        getInstitution(school);
    }
})

// 切换学院的响应事件
$("#select-institution").change(function () {
    let school = $("#select-college").children("option:selected").text();
    let institution = $(this).children("option:selected").text();
    // console.log(school,institution);
    getInstitutionGraphData(school,institution);
});


/**
 * 根据学校名获取其所有学院信息
 * @param {String} school 学校名
 */
function getInstitution(school){
    $.ajax({
        type: "get",
        url: "institution",
        data: {"school" : school},
        dataType: "json",
        success: function (institution) {
            setInstitution(institution, school);
            // 保存数据
            SCHOOL_LIST[school] = institution;
        },
        error: function(xhr){
            console.error("query institution error,and the status is: ", xhr.status);
        }
    });
}


/**
 * 将学院信息填充到下拉框中
 * @param {array} institution_list 学院数组
 * @param {String} school 学校
 */
function setInstitution(institution_list, school){
    if(institution_list.length <= 0){
        alert("学院数据为空");
        return;
    }
    let options = "";
    for (let i = 0; i < institution_list.length; i++) {
        options += `<option>${institution_list[i]}</option>`;
    }
    $("#select-institution").html(options);
    getInstitutionGraphData(school, institution_list[0]);
}


/**
 * 根据学校名及学院名，获取学院内的关系数据
 * @param {String} school
 * @param {String} institution
 */
function getInstitutionGraphData(school, institution){
    let file_path = `/static/relation_data/${school}${institution}.txt`;
    $.ajax({
        type: "get",
        url: file_path,
        dataType: "json",
        success: function (response) {
            reload_graph(formatGraph(response));
        },
        error : function (xhr) {
            if (xhr.status == 404){
                alert("当前学院尚无数据！");
                return;
            }
            alert("数据请求出错，请稍后再试");
        }
    });
}


/**
 * 规格化关系图数据，使之可以生成echarts可用的数据格式
 * @param data
 * @returns {{nodes: Array, links: Array, community: *}}
 */
function formatGraph(data){
    // console.log(data,typeof (data));
    if (typeof (data) == "string"){
        data = JSON.parse(data);
        console.log(typeof(data));
    }

    let back_data = {
        "nodes" : [],
        "links" : [],
        "community" : data['community_data']
    };

    let nodes = data['nodes'];

    for(let index in nodes){
        let node = nodes[index];
        node['label'] = node['name'];
        node['name'] = String(node['teacherId']);
        node['symbolSize'] = parseInt(node['centrality'] * 30 + 5);
        node['category'] = node['class'] - 1;
        node.draggable= true;

        if(data.core_node.indexOf(node["teacherId"]) >= 0){
            node["itemStyle"]= {
                "normal": {
                    "borderColor": 'yellow',
                    "borderWidth": 5,
                    "shadowBlur": 10,
                    "shadowColor": 'rgba(0, 0, 0, 0.3)'
                }
            }
        }

        delete node["teacherId"];
        delete node["class"];
        delete node["centrality"];
        back_data["nodes"].push(node);
    }

    let links = data['edges'];
    for(let index in links){
        let link = links[index];
        if(!("source" in link && "target" in link))
            continue;
        link["source"] = String(link["source"]);
        link["target"] = String(link["target"]);
        link["value"] = link["weight"];
        delete link["weight"];
        back_data['links'].push(link)
    }

    return back_data;
}
