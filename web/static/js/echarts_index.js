// 用于记录本次选择的算法
var ALG_LIST = [];
//用于保存不同算法产生的值
var DATA = {};
// 保存条形图需要的社区间比较数据
var BAR_GRAPH_DATA_COMMIUNITY = {};
// 算法间比较数据
var BAR_GRAPH_DATA_ALG = {};
// 标识当前是否在运算，防止重复提交
var RUNING = false;



$("#result-list").on("click", (e)=>{
    let $target = $(e.target);
    
    if(!$target.attr("data-type")) return;

    let $bar_area = $("#bar_chart_container");

    if($target.hasClass("active")){
        $target.removeClass("active");
        $bar_area.attr("style","z-index:1");
    }else{
        $target.addClass("active").siblings("dt").removeClass("active");
        
        // "1" or "2"
        if(hot_reload_bar_graph( $target.attr("data-type"))){
            $bar_area.attr("style","z-index:20");
        }      

    }
});

// 显示结果分析
$("#result-button").click((e)=>{
    $("#result-button").toggleClass("active");
    $("#result-box").toggleClass("show-box");
});

// 显示参数配置容器
$("#setting-button").click((e)=>{
    $("#setting-button").toggleClass("active");
    $("#params-box").toggleClass("show-box");
});


/**
 * 点击复选框，选择算法
 */
$("#select-algorithm").on("click", (e)=>{
    let $target = $(e.target);
    if($target.is("input")){
        let algorithm = $target.attr("data-name");
        // 选中
        if($target.is(":checked")){
            let param = get_params(algorithm);
            let inputs = "", content;
            for (let key in param){
                inputs += `<div class="param-items">
                    <input type="text" class="params-key" value="${key}" placeholder="参数名">
                    <input type="text" class="params-value" value="${param[key]}" placeholder="参数值">
                    <i class="fa fa-plus-circle plus-icon"></i>
                    <i class="fa fa-minus-circle minus-icon"></i>
                </div>`;
            }
            // 无已存参数
            if(inputs.length < 5){
                inputs = `<div class="param-items">
                    <input type="text" class="params-key" placeholder="参数名">
                    <input type="text" class="params-value" placeholder="参数值">
                    <i class="fa fa-plus-circle plus-icon"></i>
                    <i class="fa fa-minus-circle minus-icon"></i>
                </div>`;
            }

            content = `
            <div id="param-${algorithm}" data-alg="${algorithm}" class="param-container">
                <h4 class="param-title">${algorithm}的参数</h4>
                ${inputs}
            </div>`;

            $("#params-list").prepend(content);
        }
        else{
            $(`#param-${algorithm}`).remove();
        }
    }
})

/**
 * 增/删参数项
 */
$("#params-list").on("click", (e)=>{
    let $target = $(e.target);
    // 添加参数项
    if($target.hasClass("plus-icon")){
        let insert_content = `<div class="param-items">
        <input type="text" class="params-key" placeholder="参数名">
        <input type="text" class="params-value" placeholder="参数值">
        <i class="fa fa-plus-circle plus-icon"></i>
        <i class="fa fa-minus-circle minus-icon"></i>
    </div>`;
        $target.parent().after(insert_content);
    }
    else if ($target.hasClass("minus-icon")){
        $target.parent().remove();
    }
})


// 
$("#algorithm-list").on("click", (e)=>{
    let $target = $(e.target);
    if(!$target.hasClass("active")){
        $target.addClass("active").siblings().removeClass("active");
        if(JSON.stringify(DATA) != '{}'){
            reload_graph(DATA[$target.attr("data-code")]);
            
            if($("#result-list .active").length){
                hot_reload_bar_graph($("#result-list .active")[0].getAttribute("data-type"))
            }
        }

    }
})



/**
 * 获取选定算法及其参数，用于表单提交
 * @return {"FN" : {"key1":"v1",...}, "LPA" : {...},...}
 */
function get_algorithm_and_params(){
    let alg = $("#params-box .param-container");
    let result = {};
    ALG_LIST = [];
//    console.log(alg);
    for (let i = 0; i < alg.length; i++) {
        let alg_name = alg[i].getAttribute("data-alg");
        ALG_LIST.push(alg_name);
        result[alg_name] = save_params(alg_name);
    }
//    console.log(ALG_LIST);
    return result;
}


/**
 * 将输入的参数保存到本地
 * @param {String} alg_name 算法名称，eg:FN
 * @return 对象/键值对 {}
 */
function save_params(alg_name){
    let inputs = $(`#param-${alg_name} input`), 
        param_list = {};

    for (let i = 0; i < inputs.length; i+=2) {
        let key = inputs[i], v = inputs[i+1];
        
        // 参数键值对非空
        if (key.value.trim().length != 0 && v.value.trim().length != 0){
            param_list[key.value.trim()] = v.value.trim();
        }
    }
    
    localStorage.setItem(alg_name, JSON.stringify(param_list))
    return param_list;
}

/**
 * 从本地存储获取参数值
 * @param {String} alg_name 算法名，eg : LPA
 * @return 对象/键值对 {}
 */
function get_params(alg_name){
    let param = localStorage.getItem(alg_name);
    return JSON.parse(param);
}


/**
 * 将算法返回的数据格式化为前端显示需要的数据格式
   
 * @param {json} data 算法返回的数据集, 其中 community_data 的键是 class 的值，即为社区值
 *{
 *    "nodes":[{"id": 1, "name": "张三","school": "", "insititution": "", "code": "0812", "teacherId": "", "class": 1, "centrality": 0.8889},...],
 *    "edges":[{"source": 2, "target": 1, "paper": 2, "patent": 8, "project": 1, "weight": 11},...],
 *    "community_data": [{"1": {"density": 0.6667, "transity": 0.6, "cluster": 0.5833}},...]
 *}
 * @return: object 格式
 *{
 *    "nodes":[{"name":1,"label":"张三","code":0812,"school":"","insititution":"","teacherId":"", "class": 0,"symbolSize": 10},,...],
 *    "links" : [{"source":1,"target":0,"paper":1,"patent":0,"project":0,"value":1 },...],
 *    "community_data": [{"1": {"density": 0.6667, "transity": 0.6, "cluster": 0.5833},...]
 *}
 */
function format_data_to_echarts(data){
    DATA = {};
    console.log(data);
    for(let alg_name in data){
        
        let info = data[alg_name];

        if (typeof(info) == "string") {
            info = JSON.parse(info);
        }

        DATA[alg_name]= formatGraph(info);
        console.log(DATA[alg_name]);
    }
    
    format_bar_graph_data(data);
}


/**
 * 处理返回的数据
 * @param {*} data 
 */
function updateData(data){
    //  更新侧边栏选项
    let algorithm = "";

    for(let i in ALG_LIST){
        if (i == 0){
            algorithm += `<dt class="active" data-code="${ALG_LIST[i]}">${ALG_LIST[i]}</dt>`;
        }else{
            algorithm += `<dt data-code="${ALG_LIST[i]}">${ALG_LIST[i]}</dt>`;
        }
    }
    $("#algorithm-list").html(algorithm);
    reload_graph(DATA[ALG_LIST[0]]);

}


/**
 * 
 * @param {*} data 
 */
function format_bar_graph_data(data){
    let xAxis_alg = [], legend_alg = [], series_alg = {};

    for(let alg in data){
        let info = JSON.parse(data[alg]);
        xAxis_alg.push(alg);
        // 算法间的比较
        for (let i in info['algorithm_compare']){
                let content = info["algorithm_compare"][i];
                for(let key in content){
                    if(legend_alg.indexOf(key) < 0){
                        legend_alg.push(key);
                        series_alg[key] = [];
                    }
                    series_alg[key].push(content[key]);
                }
            
        }
        
        // 社区间比较：显示community_data
        /**
         * data = [{"1": {"density": 0.1323, "transity": 0.2351, "cluster": 0.3927}},
         * {"2": {"density": 0.2444, "transity": 0.2857, "cluster": 0.22}},...]
         */
        let community = info["community_data"];

        let xAxis = [], legend = [], series = {};

        for (let i in community){
            for(let index in community[i]){
                xAxis.push("社区" + index);
                let detail = community[i][index];

                for(let key in detail){
                    if( i == 0){
                        legend.push(key);
                        series[key] = [];
                    }
                    series[key].push(detail[key]);
                }
            }
        }

        BAR_GRAPH_DATA_COMMIUNITY[alg] = {
            "xAxis" : xAxis,
            "legend" : legend,
            "series" : series
        }
    }

    BAR_GRAPH_DATA_ALG = {
        "xAxis" : xAxis_alg,
        "legend" : legend_alg,
        "series" : series_alg
    }
}

/**
 * 
 * @param {*} type 
 */
function hot_reload_bar_graph(type){
    if(type === "1"){
        // TODO  算法间比较
        reload_bar_graph(BAR_GRAPH_DATA_ALG);
    }
    else if(type === "2"){
        // 社区间比较
        let alg_name = $("#algorithm-list .active").attr("data-code");
        reload_bar_graph(BAR_GRAPH_DATA_COMMIUNITY[alg_name]);
    }
    else{
        return false;
    }
    return true;
}
