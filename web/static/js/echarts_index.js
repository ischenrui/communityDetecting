$("#result-list").on("click", (e)=>{
    let $target = $(e.target);
    let $bar_area = $("#bar_chart_container");
    if($target.hasClass("active")){
        $target.removeClass("active");
        $bar_area.attr("style","z-index:1");
    }else{
        $target.addClass("active").siblings("dt").removeClass("active");
        $bar_area.attr("style","z-index:20");
    }
});

$("#result-button").click((e)=>{
    $("#result-button").toggleClass("active");
    $("#result-box").toggleClass("show-box");
});

$("#setting-button").click((e)=>{
    $("#setting-button").toggleClass("active");
    $("#params-box").toggleClass("show-box");
});

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


$("#algorithm-list").on("click", (e)=>{
    let $target = $(e.target);
    if(!$target.hasClass("active")){
        $target.addClass("active").siblings().removeClass("active");
        if(DATA.length > 0){
            reload_graph(DATA[$target.attr("data-code")]);
        }

    }
})


// 用于记录本次选择的算法
var ALG_LIST = [];
//用于保存不同算法产生的值
var DATA = {};
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

    DATA = data;
    for(let alg_name in DATA){
        for(let i in DATA[alg_name].nodes){
            let node = DATA[alg_name].nodes[i];
            node['symbolSize'] = parseInt(node['centrality'] * 20 + 5);
        }
    }

    reload_graph(DATA[ALG_LIST[0]]);
}


