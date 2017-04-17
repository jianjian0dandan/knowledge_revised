function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().substr(0,10);
};
// 柱状图
var location_url='/group/group_geo/?g_name='+group_name+'&submit_user='+submit_user;
$.ajax({
    url: location_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:result
});
var main_place,end_place,map_data;
function result(data) {
    Draw_top_location(data.activity_geo_distribution_date);
    area_table(data.activity_geo_vary);
    main_place=data.main_start_geo;
    end_place=data.main_end_geo;
    map_data=data.vary_detail_geo;
}

function Draw_top_location(data){
    var timeline_data = [];
    var bar_data = [];
    var bar_data_x = [];
    var bar_data_y = [];
    for(var key in data){
        var test=[];
        for(var key0 in data[key]){
            test.push(data[key]);
        }
        if (test.length != 0){
            var key_time = getLocalTime(key);
            timeline_data.push(key_time);
            bar_data.push(data[key]);
        }
    }
    for(var i=0;i<bar_data.length;i++){
        var bar_data_x_single = [];
        var bar_data_y_single = [];
        for(var key in bar_data[i]){
            var city = key.split('\t');
            //console.log(city.pop());
            //bar_data_x_single.push(key);
            bar_data_x_single.push(city.pop());
            bar_data_y_single.push(bar_data[i][key]);
        }
        bar_data_x.push(bar_data_x_single);
        bar_data_y.push(bar_data_y_single);  //singleday
    }
    var bar_data_2 = []
    for(var j=0;j<bar_data_x.length;j++){
        var bar_data_x_2 = []
        var len = 10;
        // if(bar_data_x[j].length<10){
        //     //console.log('ddd',bar_data_x[j].length);
        //     push_null = 10 - bar_data_x[j].length;
        //     for(var m=0; m<push_null; m++){
        //         bar_data_x[j].push('');
        //         bar_data_y[j].push(0);
        //     }
        // }
        for(var i = 0;i<bar_data_x[j].length; i++){
            if(i%2 != 0){
                bar_data_x_2.push('\n'+bar_data_x[j][i]);
            }else{
                bar_data_x_2.push(bar_data_x[j][i]);
            }
        }
        bar_data_2.push(bar_data_x_2);
    }
    bar_data_x = bar_data_2;
    var myChart = echarts.init(document.getElementById('distributed'));
    var option = {
        timeline:{
            data:timeline_data,
            label : {
                formatter : function(s) {
                    var t=getLocalTime(s/1000).slice(5,10).replace(/\//g,'-');
                    return t;
                }
            },
            autoPlay : true,
            playInterval : 2000
        },
        toolbox : {
            'show':false,
            orient : 'vertical',
            x: 'right',
            y: 'center',
            'feature':{
                'mark':{'show':true},
                'dataView':{'show':true,'readOnly':false},
                'magicType':{'show':true,'type':['line','bar','stack','tiled']},
                'restore':{'show':true},
                'saveAsImage':{'show':true}
            }
        },
        options : (function () {
                var option_data = [];
                for(var i=0;i<timeline_data.length;i++){
                    var option_single_data = {};
                    option_single_data.title={'text': '' };
                    option_single_data.tooltip ={'trigger':'axis'};
                    option_single_data.calculable = true;
                    option_single_data.grid = {'y':50,'y2':100};
                    option_single_data.xAxis = [{
                        'type':'category',
                        'axisLabel':{'interval':0},
                        'data':bar_data_x[i]
                    }];
                    option_single_data.yAxis = [
                        {
                            'type':'value',
                            'name':'活跃次数',
                            //'max':53500
                        }
                    ];
                    option_single_data.series = [
                        {
                            'name':'活跃次数',
                            'type':'bar',
                            'barwidth':10,
                            'data': bar_data_y[i]
                        },

                    ];
                    option_data.push(option_single_data);
                };
                // console.log(option_data);
                return option_data;
            }
        )()
    };
    myChart.setOption(option);

};

//地域分布
var p=1,in_out;
function condition1(value) {
    if (value==1){
        p=1;
        go();
    }else if(value==2){
        $('#condition2').empty();
        in_out='out';
        p=2;
        for (var t=0;t<main_place.length;t++){
            $('#condition2').append(
                '<option>'+main_place[t][0].split('\t').pop()+'</option>'
            )
        }
    }else if (value==3){
        $('#condition2').empty();
        in_out='in';
        p=2;
        for (var i=0;i<end_place.length;i++){
            $('#condition2').append(
                '<option>'+end_place[i][0].split('\t').pop()+'</option>'
            )
        }
    }
}
var include_user_list=[];
function go() {
    var include_person='/group/group_detail/?g_name='+group_name+'&submit_user='+submit_user;
    $.ajax({
        url: include_person,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:function (data) {
            var data=eval(data)
            $.each(data,function (index,item) {
                if (item[1]==''||item[1]=='NULL'||item[1]=='unknown'){
                    include_user_list.push('<span class="uid">'+item[0]+'</span>');
                }else {
                    include_user_list.push(item[1]+'('+'<span class="uid">'+item[0]+'</span>'+')');
                }
            });
            $('#condition2').empty();
            for (var t=0;t<include_user_list.length;t++){
                $('#condition2').append(
                    '<option>'+include_user_list[t]+'</option>'
                )
            }
        }
    });
}
go();


$('#container #content_left .place .define').on('click',function () {
    $('#area').show(20);
    if (p==1){
        var reg = /.*\([^\)\(\d]*(\d+)[^\)\(\d]*\).*/;
        var str = $('#condition2').val();
        var uid = str.replace(reg, "$1");
        var person_url='/group/group_user_geo/?uid='+uid+'&submit_user='+submit_user;
        $.ajax({
            url: person_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:people
        });
    }else {
        var geo = $('#condition2').val();
        var geo_url='/group/group_location_geo/?g_name='+group_name+'&city='+geo+'&direction='+in_out+
            '&submit_user='+submit_user;
        $.ajax({
            url: geo_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:people
        });
    }

})


//=============
var line=[],city=[];
function people(data) {
    console.log(data)
    if (p==1){
        $.each(data.line,function (index,item) {
            line.push(
                [{name:item[0].split('\t').pop(),value:0}, {name:item[1].split('\t').pop(),value:0}]
            )
        });
    }else {
        $.each(data.line,function (index,item) {
            line.push(
                [{name:item[0].split('\t').pop(),value:item[2]}, {name:item[1].split('\t').pop(),value:item[2]}]
            )
        });
    }

    $.each(data.city,function (index,item) {
        city.push(
            {name:item.split('\t').pop()}
        )
    });

    require.config({
        paths: {
            echarts: '/static/js/echarts-2/build/dist',
        }
    });
    require(
        [
            'echarts',
            'echarts/chart/map'
        ],
        function (ec) {
            $('#area').empty();
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('area'));
            var option = {
                color: ['gold','aqua','lime'],
                tooltip : {
                    trigger: 'item',
                    formatter: function (v) {
                        return v.name;
                    }
                },
                dataRange: {
                    min : 0,
                    max : 100,
                    calculable : true,
                    color: ['#ff3333', 'orange', 'yellow','lime','aqua'],
                    textStyle:{
                        color:'#676767'
                    }
                },
                series : [
                    {
                        type: 'map',
                        roam: true,
                        hoverable: true,
                        mapType: 'china',
                        itemStyle:{
                            normal:{
                                borderColor:'rgba(100,149,237,1)',
                                borderWidth:0.5,
                                areaStyle:{
                                    color: '#e7e7e8'
                                }
                            },
                            emphasis:{
                                label:{
                                    show:true,
                                    areaStyle:{
                                        color: '#67b4d0'
                                    }
                                }
                            }

                        },
                        data:[],
                        geoCoord: {
                            '香港':[114.15,22.15],
                            "鹰潭": [117.03,28.14],
                            "海门":[121.15,31.89],
                            "鄂尔多斯":[109.781327,39.608266],
                            "招远":[120.38,37.35],
                            "舟山":[122.207216,29.985295],
                            "齐齐哈尔":[123.97,47.33],
                            "盐城":[120.13,33.38],
                            "赤峰":[118.87,42.28],
                            "青岛":[120.33,36.07],
                            "乳山":[121.52,36.89],
                            "金昌":[102.188043,38.520089],
                            "泉州":[118.58,24.93],
                            "莱西":[120.53,36.86],
                            "日照":[119.46,35.42],
                            "胶南":[119.97,35.88],
                            "南通":[121.05,32.08],
                            "拉萨":[91.11,29.97],
                            "云浮":[112.02,22.93],
                            "梅州":[116.1,24.55],
                            "文登":[122.05,37.2],
                            "上海":[121.48,31.22],
                            "攀枝花":[101.718637,26.582347],
                            "威海":[122.1,37.5],
                            "承德":[117.93,40.97],
                            "厦门":[118.1,24.46],
                            "汕尾":[115.375279,22.786211],
                            "潮州":[116.63,23.68],
                            "丹东":[124.37,40.13],
                            "太仓":[121.1,31.45],
                            "曲靖":[103.79,25.51],
                            "烟台":[121.39,37.52],
                            "福州":[119.3,26.08],
                            "瓦房店":[121.979603,39.627114],
                            "即墨":[120.45,36.38],
                            "抚顺":[123.97,41.97],
                            "玉溪":[102.52,24.35],
                            "张家口":[114.87,40.82],
                            "阳泉":[113.57,37.85],
                            "莱州":[119.942327,37.177017],
                            "湖州":[120.1,30.86],
                            "汕头":[116.69,23.39],
                            "昆山":[120.95,31.39],
                            "宁波":[121.56,29.86],
                            "湛江":[110.359377,21.270708],
                            "揭阳":[116.35,23.55],
                            "荣成":[122.41,37.16],
                            "连云港":[119.16,34.59],
                            "葫芦岛":[120.836932,40.711052],
                            "常熟":[120.74,31.64],
                            "东莞":[113.75,23.04],
                            "河源":[114.68,23.73],
                            "淮安":[119.15,33.5],
                            "泰州":[119.9,32.49],
                            "南宁":[108.33,22.84],
                            "营口":[122.18,40.65],
                            "惠州":[114.4,23.09],
                            "江阴":[120.26,31.91],
                            "蓬莱":[120.75,37.8],
                            "韶关":[113.62,24.84],
                            "嘉峪关":[98.289152,39.77313],
                            "广州":[113.23,23.16],
                            "延安":[109.47,36.6],
                            "太原":[112.53,37.87],
                            "清远":[113.01,23.7],
                            "中山":[113.38,22.52],
                            "昆明":[102.73,25.04],
                            "寿光":[118.73,36.86],
                            "盘锦":[122.070714,41.119997],
                            "长治":[113.08,36.18],
                            "深圳":[114.07,22.62],
                            "珠海":[113.52,22.3],
                            "宿迁":[118.3,33.96],
                            "咸阳":[108.72,34.36],
                            "铜川":[109.11,35.09],
                            "平度":[119.97,36.77],
                            "佛山":[113.11,23.05],
                            "海口":[110.35,20.02],
                            "江门":[113.06,22.61],
                            "章丘":[117.53,36.72],
                            "肇庆":[112.44,23.05],
                            "大连":[121.62,38.92],
                            "临汾":[111.5,36.08],
                            "吴江":[120.63,31.16],
                            "石嘴山":[106.39,39.04],
                            "沈阳":[123.38,41.8],
                            "苏州":[120.62,31.32],
                            "茂名":[110.88,21.68],
                            "嘉兴":[120.76,30.77],
                            "长春":[125.35,43.88],
                            "胶州":[120.03336,36.264622],
                            "银川":[106.27,38.47],
                            "张家港":[120.555821,31.875428],
                            "三门峡":[111.19,34.76],
                            "锦州":[121.15,41.13],
                            "南昌":[115.89,28.68],
                            "柳州":[109.4,24.33],
                            "三亚":[109.511909,18.252847],
                            "自贡":[104.778442,29.33903],
                            "吉林":[126.57,43.87],
                            "阳江":[111.95,21.85],
                            "泸州":[105.39,28.91],
                            "西宁":[101.74,36.56],
                            "宜宾":[104.56,29.77],
                            "呼和浩特":[111.65,40.82],
                            "成都":[104.06,30.67],
                            "大同":[113.3,40.12],
                            "镇江":[119.44,32.2],
                            "桂林":[110.28,25.29],
                            "张家界":[110.479191,29.117096],
                            "宜兴":[119.82,31.36],
                            "北海":[109.12,21.49],
                            "西安":[108.95,34.27],
                            "金坛":[119.56,31.74],
                            "东营":[118.49,37.46],
                            "牡丹江":[129.58,44.6],
                            "遵义":[106.9,27.7],
                            "绍兴":[120.58,30.01],
                            "扬州":[119.42,32.39],
                            "常州":[119.95,31.79],
                            "潍坊":[119.1,36.62],
                            "重庆":[106.54,29.59],
                            "台州":[121.420757,28.656386],
                            "南京":[118.78,32.04],
                            "滨州":[118.03,37.36],
                            "贵阳":[106.71,26.57],
                            "无锡":[120.29,31.59],
                            "本溪":[123.73,41.3],
                            "克拉玛依":[84.77,45.59],
                            "渭南":[109.5,34.52],
                            "马鞍山":[118.48,31.56],
                            "宝鸡":[107.15,34.38],
                            "焦作":[113.21,35.24],
                            "句容":[119.16,31.95],
                            "北京":[116.46,39.92],
                            "徐州":[117.2,34.26],
                            "衡水":[115.72,37.72],
                            "包头":[110,40.58],
                            "绵阳":[104.73,31.48],
                            "乌鲁木齐":[87.68,43.77],
                            "枣庄":[117.57,34.86],
                            "杭州":[120.19,30.26],
                            "淄博":[118.05,36.78],
                            "鞍山":[122.85,41.12],
                            "溧阳":[119.48,31.43],
                            "库尔勒":[86.06,41.68],
                            "安阳":[114.35,36.1],
                            "开封":[114.35,34.79],
                            "济南":[117,36.65],
                            "德阳":[104.37,31.13],
                            "温州":[120.65,28.01],
                            "九江":[115.97,29.71],
                            "邯郸":[114.47,36.6],
                            "临安":[119.72,30.23],
                            "兰州":[103.73,36.03],
                            "沧州":[116.83,38.33],
                            "临沂":[118.35,35.05],
                            "南充":[106.110698,30.837793],
                            "天津":[117.2,39.13],
                            "富阳":[119.95,30.07],
                            "泰安":[117.13,36.18],
                            "诸暨":[120.23,29.71],
                            "郑州":[113.65,34.76],
                            "哈尔滨":[126.63,45.75],
                            "聊城":[115.97,36.45],
                            "芜湖":[118.38,31.33],
                            "唐山":[118.02,39.63],
                            "平顶山":[113.29,33.75],
                            "邢台":[114.48,37.05],
                            "德州":[116.29,37.45],
                            "济宁":[116.59,35.38],
                            "荆州":[112.239741,30.335165],
                            "宜昌":[111.3,30.7],
                            "义乌":[120.06,29.32],
                            "丽水":[119.92,28.45],
                            "洛阳":[112.44,34.7],
                            "秦皇岛":[119.57,39.95],
                            "株洲":[113.16,27.83],
                            "石家庄":[114.48,38.03],
                            "莱芜":[117.67,36.19],
                            "常德":[111.69,29.05],
                            "保定":[115.48,38.85],
                            "湘潭":[112.91,27.87],
                            "金华":[119.64,29.12],
                            "岳阳":[113.09,29.37],
                            "长沙":[113,28.21],
                            "衢州":[118.88,28.97],
                            "廊坊":[116.7,39.53],
                            "菏泽":[115.480656,35.23375],
                            "合肥":[117.27,31.86],
                            "武汉":[114.31,30.52],
                            "大庆":[125.03,46.58],
                            "鹰潭":[28.14, 117.03],
                            '安徽':[117.17,31.52],
                            '澳门':[115.07,21.53],
                            '福建':[119.18,26.05],
                            '甘肃':[103.51,36.04],
                            '广东':[113.14,23.08],
                            '广西':[108.19,22.48],
                            '贵州':[106.42,26.35],
                            '海南':[110.20,20.02],
                            '河北':[114.30,38.02],
                            '河南':[113.40,34.46],
                            '黑龙江':[126.36,45.44],
                            '湖北':[114.17,30.35],
                            '湖南':[112.59,28.12],
                            '吉林':[125.19,43.54],
                            '江苏':[118.46,32.03],
                            '江西':[115.55,28.40],
                            '辽宁':[123.25,41.48],
                            '内蒙古':[111.41,40.48],
                            '青海':[101.48,36.38],
                            '山东':[117.00,36.40],
                            '山西':[112.33,37.54],
                            '陕西':[108.57,34.17],
                            '四川':[104.04,30.40],
                            '台湾':[121.30,25.03],
                            '西藏':[91.08,29.39],
                            '香港':[115.12,21.23],
                            '新疆':[87.36,43.45],
                            '云南':[102.42,25.04],
                            '浙江':[120.10,30.16],
                            '宁夏':[106.11,37.59],
                        },
                    },
                    {
                        type: 'map',
                        mapType: 'china',
                        data:[],
                        markLine : {
                            smooth:true,
                            effect : {
                                show: true,
                                scaleSize: 1,
                                period: 30,
                                color: '#fff',
                                shadowBlur: 10
                            },
                            itemStyle : {
                                normal: {
                                    borderWidth:1,
                                    lineStyle: {
                                        type: 'solid',
                                        shadowBlur: 10
                                    },
                                }
                            },
                            data : line,
                            // data : [
                            //     [{name:'临沂'}, {name:'上海',value:95}],
                            // ]
                        },
                        markPoint : {
                            symbol:'emptyCircle',
                            symbolSize : function (v){
                                return 10 + v/10
                            },
                            effect : {
                                show: true,
                                shadowBlur : 0
                            },
                            itemStyle:{
                                normal:{
                                    label:{show:false}
                                },
                                emphasis: {
                                    label:{position:'top'}
                                }
                            },
                            data : city,
                            // data : [
                            //     {name:'上海',value:95},
                            // ]
                        }
                    }
                ]
            };
            myChart.setOption(option);
            // var ecConfig = require('echarts/config');
            // myChart.on(ecConfig.EVENT.HOVER, function (param){
            //     var selected = param.name;
            // });
            line=[],city=[];
        }
    );

}


//表格
function area_table(data) {
    var data_tab=[];
    for (var key in data){
        this_list=key.split('&');
        this_list.push(data[key])
        data_tab.push(this_list);
    }
    if (data_tab.length==0){
        $('#area_table').css({display:'none'})
    }else {
        $('#area_table').bootstrapTable('load', data_tab);
        $('#area_table').bootstrapTable({
            data:data_tab,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: 5,//单页记录数
            pageList: [5, 10, 20],//分页步进值
            sidePagination: "client",//服务端分页
            searchAlign: "left",
            searchOnEnterKey: false,//回车搜索
            showRefresh: false,//刷新按钮
            showColumns: false,//列选择按钮
            buttonsAlign: "right",//按钮对齐方式
            locale: "zh-CN",//中文支持
            detailView: false,
            showToggle:false,
            sortName:'bci',
            sortOrder:"desc",
            columns: [
                {
                    title: "起始地",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row[0]==''||row[0]=='NULL'){
                            return '未知';
                        }else {
                            return row[0].split('\t').pop();
                        }
                    }
                },
                {
                    title: "目的地",//标题
                    field: "user",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row[1]==''||row[1]=='NULL'){
                            return '未知';
                        }else {
                            return row[1].split('\t').pop();
                        }
                    }
                },
                {
                    title: "人次",//标题
                    field: "influ",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row[2]==''||row[2]=='NULL'){
                            return 0;
                        }else {
                            return row[2];
                        }
                    },
                },

            ],
            // onClickRow: function (row, tr) {
            //     if ($(tr.context).index()==2) {
            //         del_eventuid=row[0];
            //         $('#del_ject').modal("show");
            //     }
            // }
        });
    }

};

//

