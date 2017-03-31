//包含事件
var things_url='/theme/theme_detail/?theme_name='+theme_name+'&submit_user='+submit_user;
$.ajax({
    url: things_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:things
});
function things(data) {
    var data = eval(data);
    $('#things').bootstrapTable('load', data);
    $('#things').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40, 80],//分页步进值
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
                title: "事件名称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[1];
                }
            },
            {
                title: "事件类型",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==''||row[2]=='NULL'||row[2]=='unknown'){
                        return '暂无';
                    }else {
                        return row[2];
                    }
                }
            },
            {
                title: "发生时间",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[3]==''||row[3]=='NULL'||row[3]=='unknown'){
                        return '暂无';
                    }else {
                        return row[3];
                    }
                },
            },
            {
                title: "发生地点",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[4]==''||row[4]=='NULL'||row[4]=='unknown'){
                        return '暂无';
                    }else {
                        return row[4];
                    }
                },
            },
            {
                title: "参与人数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[5]==''||row[5]=='NULL'||row[5]=='unknown'){
                        return '暂无';
                    }else {
                        return row[5];
                    }
                },
            },
            {
                title: "微博数量",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[6]==''||row[6]=='NULL'||row[6]=='unknown'){
                        return '暂无';
                    }else {
                        return row[6];
                    }
                },
            },
            {
                title: "自动标签",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[7].length==0||row[7]==''){
                        return '暂无';
                    }else {
                        var key='';
                        for (var k=0;k<row[7].length;k++){
                            key+=row[7][k]+' ';
                        }
                        return key;
                    }
                },
            },
            {
                title: "业务标签",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[8].length==0||row[8]==''){
                        return '暂无';
                    }else {
                        var tag='';
                        for (var k=0;k<row[8].length;k++){
                            tag+=row[8][k]+' ';
                        }
                        return tag;
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
};

//时间分析--鱼骨图
var fish_url='/theme/theme_analysis_flow/?theme_name='+theme_name+'&submit_user='+submit_user;
$.ajax({
    url: fish_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:fish
});
var finshdata = [];
function fish(data) {
    var data=eval(data);
    $.each(data,function (index,item) {
        finshdata.push(
            {'事件ID':item[0],'微博内容':item[1],'时间':item[2]}
        );
    })
    $(".fishBone").fishBone(finshdata);
}


//地域分析
var place_url='/theme/theme_analysis_geo/?theme_name='+theme_name+'&submit_user='+submit_user;
$.ajax({
    url: place_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:place
});
function place(data) {
    var data=eval(data);
    var place_x=[],place_series=[],legends=[];
    $.each(data.top_city,function (index,item) {
        place_x.push(item);
    })
    for (var key in data.event_city){
        legends.push(key);
        place_series.push(
            {
                name: key,
                type: 'bar',
                stack: '数量',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: data.event_city[key]
            }
        )
    }
    var myChart = echarts.init(document.getElementById('area'));
    var option = {
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: legends
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis:  {
            type: 'category',
            data: place_x
        },
        yAxis: {
            type: 'value'
        },
        series: place_series
    };
    myChart.setOption(option);
}

//网络分析
var network_url='/theme/theme_analysis_net/?theme_name='+theme_name+'&submit_user='+submit_user;
$.ajax({
    url: network_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:network
});
var rel_table={
    "join":"参与事件",
    "discuss":"参与舆论",
    "other_relation":"其他关系",
    "contain":"主题关联",
    "event_other":"其他关系",
    "friend":"交互",
    "colleague":"业务关联",
    "organization_tag":"其他关系",
    "friend":"交互",
    "relative":"亲属",
    "leader":"上下级关系",
    "colleague":"自述关联",
    "ip_relation":"IP关联",
    "user_tag":"其他关系",
};
function network(data) {
    var data = eval(data);
    $('#container #content_left .network_analysis .net_detail .detail-1 .det-1').text(data.relation_count);
    $('#container #content_left .network_analysis .net_detail .detail-1 .det-2').text(data.relation_degree.toFixed(2));
    $('#container #content_left .network_analysis .net_detail .detail-1 .det-3').text(data.conclusion);
    $('#network_list').bootstrapTable('load', data.relation_table);
    $('#network_list').bootstrapTable({
        data:data.relation_table,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40, 80],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: false,//回车搜索
        showRefresh: true,//刷新按钮
        showColumns: true,//列选择按钮
        buttonsAlign: "right",//按钮对齐方式
        locale: "zh-CN",//中文支持
        detailView: false,
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "事件名称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[0];
                }
            },
            {
                title: "关系",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    console.log(rel_table[row[1]])
                    return rel_table[row[1]];
                }
            },
            {
                title: "事件名称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[2];
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
};

//=============话题分析
require.config({
    paths: {
        echarts: '/static/js/echarts-2/build/dist',
    }
});
//----自动标签
require(
    [
        'echarts',
        'echarts/chart/wordCloud'
    ],
    function (ec) {
        // 基于准备好的dom，初始化echarts图表
        var myChart = ec.init(document.getElementById('tag_left'));

        function createRandomItemStyle() {
            return {
                normal: {
                    color: 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')'
                }
            };
        }

        option = {
            title: {
                text: '关键词',
            },
            tooltip: {
                show: true
            },
            series: [{
                name: 'Google Trends',
                type: 'wordCloud',
                size: ['80%', '80%'],
                textRotation : [0, 45, 90, -45],
                textPadding: 0,
                autoSize: {
                    enable: true,
                    minSize: 14
                },
                data: [
                    {
                        name: "Sam S Club",
                        value: 10000,
                        itemStyle: {
                            normal: {
                                color: 'black'
                            }
                        }
                    },
                    {
                        name: "Macys",
                        value: 6181,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Amy Schumer",
                        value: 4386,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Jurassic World",
                        value: 4055,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Charter Communications",
                        value: 2467,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Chick Fil A",
                        value: 2244,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Planet Fitness",
                        value: 1898,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Pitch Perfect",
                        value: 1484,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Express",
                        value: 1112,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Home",
                        value: 965,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Johnny Depp",
                        value: 847,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lena Dunham",
                        value: 582,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lewis Hamilton",
                        value: 555,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "KXAN",
                        value: 550,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Mary Ellen Mark",
                        value: 462,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Farrah Abraham",
                        value: 366,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Rita Ora",
                        value: 360,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Serena Williams",
                        value: 282,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "NCAA baseball tournament",
                        value: 273,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Point Break",
                        value: 265,
                        itemStyle: createRandomItemStyle()
                    }
                ]
            }]
        };

        myChart.setOption(option);
        var ecConfig = require('echarts/config');
        myChart.on(ecConfig.EVENT.HOVER, function (param){
            var selected = param.name;
        });
    }
);

//----微话题
require(
    [
        'echarts',
        'echarts/chart/wordCloud'
    ],
    function (ec) {
        // 基于准备好的dom，初始化echarts图表
        var myChart = ec.init(document.getElementById('tag_right'));

        function createRandomItemStyle() {
            return {
                normal: {
                    color: 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')'
                }
            };
        }

        option = {
            title: {
                text: '微话题',
            },
            tooltip: {
                show: true
            },
            series: [{
                name: 'Google Trends',
                type: 'wordCloud',
                size: ['80%', '80%'],
                textRotation : [0, 45, 90, -45],
                textPadding: 0,
                autoSize: {
                    enable: true,
                    minSize: 14
                },
                data: [
                    {
                        name: "Sam S Club",
                        value: 10000,
                        itemStyle: {
                            normal: {
                                color: 'black'
                            }
                        }
                    },
                    {
                        name: "Macys",
                        value: 6181,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Amy Schumer",
                        value: 4386,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Jurassic World",
                        value: 4055,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Charter Communications",
                        value: 2467,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Chick Fil A",
                        value: 2244,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Planet Fitness",
                        value: 1898,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Pitch Perfect",
                        value: 1484,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Express",
                        value: 1112,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Home",
                        value: 965,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Johnny Depp",
                        value: 847,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lena Dunham",
                        value: 582,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lewis Hamilton",
                        value: 555,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "KXAN",
                        value: 550,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Mary Ellen Mark",
                        value: 462,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Farrah Abraham",
                        value: 366,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Rita Ora",
                        value: 360,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Serena Williams",
                        value: 282,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "NCAA baseball tournament",
                        value: 273,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Point Break",
                        value: 265,
                        itemStyle: createRandomItemStyle()
                    }
                ]
            }]
        };

        myChart.setOption(option);
        var ecConfig = require('echarts/config');
        myChart.on(ecConfig.EVENT.HOVER, function (param){
            var selected = param.name;
        });
    }
);

//============人物分析
var character_url='';
$.ajax({
    url: character_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:character
});
function character(data) {
    var data = eval(data);
    $('#ranking').bootstrapTable('load', data);
    $('#ranking').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40, 80],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: false,//回车搜索
        showRefresh: true,//刷新按钮
        showColumns: true,//列选择按钮
        buttonsAlign: "right",//按钮对齐方式
        locale: "zh-CN",//中文支持
        detailView: false,
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "UID",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return index+1;
                }
            },
            {
                title: "人物名",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                }
            },
            {
                title: "重要度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "参与事件数量",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "参与事件",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

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
};
//----人物自动标签
require(
    [
        'echarts',
        'echarts/chart/wordCloud'
    ],
    function (ec) {
        // 基于准备好的dom，初始化echarts图表
        var myChart = ec.init(document.getElementById('label_left'));

        function createRandomItemStyle() {
            return {
                normal: {
                    color: 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')'
                }
            };
        }

        option = {
            title: {
                text: '关键词',
            },
            tooltip: {
                show: true
            },
            series: [{
                name: 'Google Trends',
                type: 'wordCloud',
                size: ['80%', '80%'],
                textRotation : [0, 45, 90, -45],
                textPadding: 0,
                autoSize: {
                    enable: true,
                    minSize: 14
                },
                data: [
                    {
                        name: "Sam S Club",
                        value: 10000,
                        itemStyle: {
                            normal: {
                                color: 'black'
                            }
                        }
                    },
                    {
                        name: "Macys",
                        value: 6181,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Amy Schumer",
                        value: 4386,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Jurassic World",
                        value: 4055,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Charter Communications",
                        value: 2467,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Chick Fil A",
                        value: 2244,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Planet Fitness",
                        value: 1898,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Pitch Perfect",
                        value: 1484,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Express",
                        value: 1112,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Home",
                        value: 965,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Johnny Depp",
                        value: 847,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lena Dunham",
                        value: 582,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lewis Hamilton",
                        value: 555,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "KXAN",
                        value: 550,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Mary Ellen Mark",
                        value: 462,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Farrah Abraham",
                        value: 366,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Rita Ora",
                        value: 360,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Serena Williams",
                        value: 282,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "NCAA baseball tournament",
                        value: 273,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Point Break",
                        value: 265,
                        itemStyle: createRandomItemStyle()
                    }
                ]
            }]
        };

        myChart.setOption(option);
        var ecConfig = require('echarts/config');
        myChart.on(ecConfig.EVENT.HOVER, function (param){
            var selected = param.name;
        });
    }
);

//----人物业务标签
require(
    [
        'echarts',
        'echarts/chart/wordCloud'
    ],
    function (ec) {
        // 基于准备好的dom，初始化echarts图表
        var myChart = ec.init(document.getElementById('label_right'));

        function createRandomItemStyle() {
            return {
                normal: {
                    color: 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')'
                }
            };
        }

        option = {
            title: {
                text: '微话题',
            },
            tooltip: {
                show: true
            },
            series: [{
                name: 'Google Trends',
                type: 'wordCloud',
                size: ['80%', '80%'],
                textRotation : [0, 45, 90, -45],
                textPadding: 0,
                autoSize: {
                    enable: true,
                    minSize: 14
                },
                data: [
                    {
                        name: "Sam S Club",
                        value: 10000,
                        itemStyle: {
                            normal: {
                                color: 'black'
                            }
                        }
                    },
                    {
                        name: "Macys",
                        value: 6181,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Amy Schumer",
                        value: 4386,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Jurassic World",
                        value: 4055,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Charter Communications",
                        value: 2467,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Chick Fil A",
                        value: 2244,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Planet Fitness",
                        value: 1898,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Pitch Perfect",
                        value: 1484,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Express",
                        value: 1112,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Home",
                        value: 965,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Johnny Depp",
                        value: 847,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lena Dunham",
                        value: 582,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Lewis Hamilton",
                        value: 555,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "KXAN",
                        value: 550,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Mary Ellen Mark",
                        value: 462,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Farrah Abraham",
                        value: 366,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Rita Ora",
                        value: 360,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Serena Williams",
                        value: 282,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "NCAA baseball tournament",
                        value: 273,
                        itemStyle: createRandomItemStyle()
                    },
                    {
                        name: "Point Break",
                        value: 265,
                        itemStyle: createRandomItemStyle()
                    }
                ]
            }]
        };

        myChart.setOption(option);
        var ecConfig = require('echarts/config');
        myChart.on(ecConfig.EVENT.HOVER, function (param){
            var selected = param.name;
        });
    }
);


