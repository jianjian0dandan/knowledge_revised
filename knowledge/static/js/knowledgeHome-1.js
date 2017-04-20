 var map_url='/index/get_index_map/';
 $.ajax({
     url: map_url,
     type: 'GET',
     dataType: 'json',
     async: true,
     success:map_geo
 });
 
 function map_geo(data) {
     var geo=eval(data);
     var myChart = echarts.init(document.getElementById('statis-3'));
    option = {
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
                zoom:1.3,
                aspectScale: 1,
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
                data:geo
            }
        ]
    };

// 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

 }

