bar_graph_option = {
    // color: ['#003366', '#006699', '#4cabce', '#e5323e'],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['学院', '学校', '学科', '全国']
    },
    toolbox: {
        show: true,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            axisTick: {show: true},
            data: ['LPA', 'FN', 'Clauset', 'Infomap', 'Louvain', "Wlaktrap"]
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: [
        {
            name: '学院',
            type: 'bar',
            data: [320, 332, 301, 334, 234, 290]
        },
        {
            name: '学校',
            type: 'bar',
            data: [220, 182, 234, 290, 301, 334]
        },
        {
            name: '学科',
            type: 'bar',
            data: [150, 232,154, 190, 232,154]
        },
        {
            name: '全国',
            type: 'bar',
            data: [98, 232,154, 101, 99, 40]
        }
    ]
};


function reload_bar_graph(data){

}

var barChart = echarts.init(document.getElementById('bar_chart'));
barChart.setOption(bar_graph_option);