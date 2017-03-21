//包含事件
var things_url='';
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
                    return index+1;
                }
            },
            {
                title: "时间类型",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

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

                },
            },
            {
                title: "业务标记",//标题
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

//时间分析--鱼骨图
finshdata = [
    {'审理时间':'2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-12-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
    {'审理时间': '2014-15-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号'},
    {'审理时间': '2014-18-20 至 2014-12-20','承办庭室':'XXXX','承办法官':'XXX','承办法院':'XXXXXXX法院','案件状态':'XX','案号':'(XXXX)XXXXXX第XXXX号(当前案件)'},
];
$(".fishBone").fishBone(finshdata);

//地域分析
var myChart = echarts.init(document.getElementById('area'));
var option = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data: ['直接访问', '邮件营销','联盟广告','视频广告','搜索引擎']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        type: 'category',
        data: ['周一','周二','周三','周四','周五','周六','周日']

    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '直接访问',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [320, 302, 301, 334, 390, 330, 320]
        },
        {
            name: '邮件营销',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
            name: '联盟广告',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [220, 182, 191, 234, 290, 330, 310]
        },
        {
            name: '视频广告',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [150, 212, 201, 154, 190, 330, 410]
        },
        {
            name: '搜索引擎',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [820, 832, 901, 934, 1290, 1330, 1320]
        }
    ]
};
myChart.setOption(option);

//网络分析
var network_url='';
$.ajax({
    url: network_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:network
});
function network(data) {
    var data = eval(data);
    $('#network_list').bootstrapTable('load', data);
    $('#network_list').bootstrapTable({
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
                title: "事件名称",//标题
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
                title: "关系",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

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


