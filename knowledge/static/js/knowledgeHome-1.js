// var map_url='';
// $.ajax({
//     url: map_url,
//     type: 'GET',
//     dataType: 'json',
//     async: true,
//     success:map_geo
// });
// function map_geo(data) {
//     var geo=eval(data);
//
// }

var myChart = echarts.init(document.getElementById('statis-3'));
// 指定图表的配置项和数据
function randomData() {
    return Math.round(Math.random()*1000);
}

option = {
    tooltip: {
        trigger: 'item'
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
            color: '#fff',
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
            label: {
                normal: {
                    show: true,
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

// option = {
//     tooltip : {
//         trigger: 'item'
//     },
//     geo: {
//         map: 'china',
//         label: {
//             emphasis: {
//                 show: true,
//             }
//         },
//         roam: true,
//         itemStyle: {
//             normal: {
//                 areaColor: '#142d41',
//                 borderColor: '#477bc4'
//             },
//             emphasis: {
//                 areaColor: '#67b4d0'
//             }
//         }
//     },
//     series : [
//         {
//             type: 'scatter',
//             coordinateSystem: 'geo',
//             data: convertData(data),
//             symbolSize: function (val) {
//                 return val[2] / 10;
//             },
//             label: {
//                 normal: {
//                     formatter: '{b}',
//                     position: 'right',
//                     show: false
//                 },
//                 emphasis: {
//                     show: true
//                 }
//             },
//             itemStyle: {
//                 normal: {
//                     color: '#fff'
//                 }
//             }
//         },
//         {
//             name: 'Top 5',
//             type: 'effectScatter',
//             coordinateSystem: 'geo',
//             data: convertData(data.sort(function (a, b) {
//                 return b.value - a.value;
//             }).slice(0, 6)),
//             symbolSize: function (val) {
//                 return val[2] / 10;
//             },
//             showEffectOn: 'render',
//             rippleEffect: {
//                 brushType: 'stroke'
//             },
//             hoverAnimation: true,
//             label: {
//                 normal: {
//                     formatter: '{b}',
//                     position: 'right',
//                     show: true
//                 }
//             },
//             itemStyle: {
//                 normal: {
//                     color: '#fff',
//                     shadowBlur: 10,
//                     shadowColor: '#333'
//                 }
//             },
//             zlevel: 1
//         }
//     ]
// };

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);