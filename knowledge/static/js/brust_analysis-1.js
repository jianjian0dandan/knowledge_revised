var myChart = echarts.init(document.getElementById('forecast_img'));
var option = {
    title : {
        // text: '某楼盘销售情况',
        // subtext: '纯属虚构'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        // data:['欺诈电话']
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data: ['周一','周二','周三','周四','周五','周六','周日'],
            axisLabel: {
                textStyle: {
                    color: 'black',
                    fontFamily: '微软雅黑',
                    fontSize: 14,
                },
            }
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel: {
                formatter: '{value} 次',
                textStyle: {
                    color: 'black',
                    fontFamily: '微软雅黑',
                    fontSize: 14,
                },
            }
        }
    ],
    series : [
        {
            // name:'欺诈电话',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:[11, 11, 15, 13, 12, 13, 10],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
    ]
};
// 为echarts对象加载数据
myChart.setOption(option);
