// 热度走势图---折线图
var myChart = echarts.init(document.getElementById('hot_trend'));
option = {
    title : {
        text: '情绪曲线图',
        left:'center'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['意向','预购','成交'],
        top:'8%',
        right:'0%'
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'成交',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:[10, 12, 21, 54, 260, 830, 710]
        },
        {
            name:'预购',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:[30, 182, 434, 791, 390, 30, 10]
        },
        {
            name:'意向',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:[1320, 1132, 601, 234, 120, 90, 20]
        }
    ]
};
myChart.setOption(option);

// 地域走势图---地图
var myChart = echarts.init(document.getElementById('place_trend'));
function randomData() {
    return Math.round(Math.random()*1000);
}
option = {
    title: {
        text: '地域统计图',
        left:'center'
    },
    tooltip: {
        trigger: 'item',
    },
    visualMap: {
        min: 0,
        max: 2500,
        left: 'left',
        top: 'bottom',
        itemWidth: 20,
        itemHeight: 80,
        text: ['高','低'],           // 文本，默认为数值文本
        inRange: {
            color: ['#e0ffff', '#006edd']
        },
        textStyle: {
            color: '#8e8e8e',
            fontSize: 12,
        },
        calculable: true
    },
    series: [
        {
            name:'地理位置',
            type: 'map',
            mapType: 'china',
            roam: true,
            layoutCenter:  ['50%', '50%'],
            layoutSize: 520,
            label: {
                normal: {
                    show: false,
                    areaColor: '#142d41',
                    borderColor: '#477bc4'
                },
                emphasis: {
                    show: true,
                    areaColor: '#67b4d0'
                }
            },
            data:[
                {name: '北京',value: 231 },
                {name: '天津',value: 56 },
                {name: '上海',value: 465 },
                {name: '广东',value: 345 },
                {name: '台湾',value: 56 },
                {name: '香港',value: 67 },
                {name: '澳门',value: 89 }
            ]
        }
    ]
};
myChart.setOption(option);

// 话题集合图---字符云


// 情绪走势图---折线图
var myChart = echarts.init(document.getElementById('mood_trend'));
var option = {
    title: {
        text: '事件热度走势图',
        left:'center',
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data:['原创','转发'],
        top:'10%',
        right:'0'
    },
    xAxis:  {
        type: 'category',
        boundaryGap: false,
        data: ['周一','周二','周三','周四','周五','周六','周日']
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            formatter: '{value} °C'
        }
    },
    series: [
        {
            name:'最高气温',
            type:'line',
            data:[11, 11, 15, 13, 12, 13, 10],
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        },
        {
            name:'最低气温',
            type:'line',
            data:[1, -2, 2, 5, 3, 2, 0],
            markPoint: {
                data: [
                    {name: '周最低', value: -2, xAxis: 1, yAxis: -1.5}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'},
                    [{
                        symbol: 'none',
                        x: '90%',
                        yAxis: 'max'
                    }, {
                        symbol: 'circle',
                        label: {
                            normal: {
                                position: 'start',
                                formatter: '最大值'
                            }
                        },
                        type: 'max',
                        name: '最高点'
                    }]
                ]
            }
        }
    ]
};
myChart.setOption(option);



