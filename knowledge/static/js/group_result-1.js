//包含人物
var include_user_url='/group/group_detail/?g_name='+group_name+'&submit_user='+submit_user;
$.ajax({
    url: include_user_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:include_user
});
function include_user(data) {
    var data = eval(data);
    $('#person').bootstrapTable('load', data);
    $('#person').bootstrapTable({
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
                title: "用户ID",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[0];
                    if (row[1]==''||row[1]=='NULL'||row[1]=='unknown'){
                        include_user_list.push('<span>'+row[0]+'</span>');
                    }else {
                        include_user_list.push(row[1]+'('+'<span>'+row[0]+'</span>'+')');
                    }
                }
            },
            {
                title: "昵称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1]==''||row[1]=='NULL'||row[1]=='unknown'){
                        return row[0];
                    }else {
                        return row[1];

                    }
                }
            },
            {
                title: "注册地",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==''||row[2]=='NULL'||row[2]=='unknown'){
                        return '未知';
                    }else {
                        return row[2];
                    }
                },
            },
            {
                title: "影响力",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[3]==''||row[3]=='NULL'||row[3]=='unknown'){
                        return 0;
                    }else {
                        return row[3].toFixed(2);
                    }
                },
            },
            {
                title: "活跃度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[4]==''||row[4]=='NULL'||row[4]=='unknown'){
                        return 0;
                    }else {
                        return row[4].toFixed(2);
                    }
                },
            },
            {
                title: "敏感度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[5]==''||row[5]=='NULL'||row[5]=='unknown'){
                        return 0;
                    }else {
                        return row[5].toFixed(2);
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
                    if (row[6]=='unknown'||row[6]==''){
                        return '暂无';
                    }else {
                        return row[6].toString().split('&').slice(0,5);
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
                    if (row[7]=='unknown'||row[7]==''){
                        return '暂无';
                    }else {
                        return row[7].toString().split('&').slice(0,5);
                    }
                    // if (row[8].length==0||row[8]==''){
                    //     return '暂无';
                    // }else {
                    //     var tag='';
                    //     for (var k=0;k<row[8].length;k++){
                    //         tag+=row[8][k]+' ';
                    //     }
                    //     return tag;
                    // }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].cellIndex==0){
                window.open('/index/person/?user_id='+row[0]);
            }
        },
    });
};

//网络分析
var network_url='/group/group_user_rank/?g_name='+group_name+'&submit_user='+submit_user;
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
                title: "UID",//标题
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
                title: "昵称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1]==''||row[1]=='NULL'||row[1]=='unknown'){
                        return row[0];
                    }else {
                        return row[1];
                    }
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
                    return row[2];
                },
            },
            {
                title: "UID",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[3];
                }
            },
            {
                title: "昵称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[4]==''||row[4]=='NULL'||row[4]=='unknown'){
                        return row[3];
                    }else {
                        return row[4];
                    }
                }
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].cellIndex==0){
                window.open('/index/person/?user_id='+row[0]);
            }else if ($element[0].cellIndex==3){
                window.open('/index/person/?user_id='+row[3]);
            };
        },
    });
};

//=============话题分析
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
require.config({
    paths: {
        echarts: '/static/js/echarts-2/build/dist',
    }
});
//----自动标签
var key_tag_url='/group/group_user_keyowrds/?g_name='+group_name+'&submit_user='+submit_user;
$.ajax({
    url: key_tag_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:key_tag
});
var key_series=[],tag_series=[];
function key_tag(data) {
    var data=eval(data);
    $.each(data.keywords,function (index,item) {
        key_series.push(
            {
                name: item[0],
                value: item[1].toFixed(2)*100,
                itemStyle: createRandomItemStyle()
            }
        )
    });
    $.each(data.hashtag,function (index,item) {
        tag_series.push(
            {
                name: item[0],
                value: item[1].toFixed(2)*100,
                itemStyle: createRandomItemStyle()
            }
        )
    });
};
if (key_series.length==0){
    $('#tag_left').html('暂无数据');
}else {
    require(
        [
            'echarts',
            'echarts/chart/wordCloud'
        ],
        //关键词
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('tag_left'));

            option = {
                title: {
                    text: '关键词',
                },
                tooltip: {
                    show: true
                },
                series: [{
                    // name: 'Google Trends',
                    type: 'wordCloud',
                    size: ['80%', '80%'],
                    textRotation : [0, 0, 0, 0],
                    textPadding: 0,
                    autoSize: {
                        enable: true,
                        minSize: 14
                    },
                    data: key_series
                }]
            };

            myChart.setOption(option);
            var ecConfig = require('echarts/config');
            myChart.on(ecConfig.EVENT.HOVER, function (param){
                var selected = param.name;
            });
        }
    );
}
if (tag_series.length==0){
    $('#tag_right').html('暂无数据');
}else {
    require(
        [
            'echarts',
            'echarts/chart/wordCloud'
        ],

        //----微话题
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('tag_right'));


            option = {
                title: {
                    text: '微话题',
                },
                tooltip: {
                    show: true
                },
                series: [{
                    // name: 'Google Trends',
                    type: 'wordCloud',
                    size: ['80%', '80%'],
                    textRotation : [0, 0, 0, 0],
                    textPadding: 0,
                    autoSize: {
                        enable: true,
                        minSize: 14
                    },
                    data: tag_series
                }]
            };

            myChart.setOption(option);
            var ecConfig = require('echarts/config');
            myChart.on(ecConfig.EVENT.HOVER, function (param){
                var selected = param.name;
            });
        }
    );
};


//============事件分析
var character_url='/group/group_event_rank/?g_name='+group_name+'&submit_user='+submit_user;
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
                title: "事件名称",//标题
                field: "event_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "关联人数",//标题
                field: "user",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.user==''||row.user=='NULL'){
                        return 0;
                    }else {
                        return row.user.length;
                    }
                }
            },
            {
                title: "重要度",//标题
                field: "influ",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='NULL'){
                        return 0;
                    }else {
                        return value.toFixed(2);
                    }
                },
            },
            {
                title: "关联用户",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.user==''||row.user=='NULL'){
                        return '暂无';
                    }else {
                        var user=row.user.splice(' ');
                        return row.user.length;
                    }
                },
            },

        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].cellIndex==0){
                window.open('/index/event/?user_id='+row.event_id);
            }
        },
    });
};


//----人物自动标签
var user_tag_url='/group/group_user_tag/?g_name='+group_name+'&submit_user='+submit_user;
$.ajax({
    url: user_tag_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:user_tag
});
var user_key_series=[],user_tag_series=[];
function user_tag(data) {
    var data = eval(data);
    $.each(data.keywords, function (index, item) {
        user_key_series.push(
            {
                name: item[0],
                value: item[1].toFixed(2) * 100,
                itemStyle: createRandomItemStyle()
            }
        )
    });
    $.each(data.mark, function (index, item) {
        user_tag_series.push(
            {
                name: item[0],
                value: item[1].toFixed(2) * 100,
                itemStyle: createRandomItemStyle()
            }
        )
    });
}
console.log(user_key_series,user_tag_series)
if (user_key_series.length==0){
    $('#label_left').html('暂无数据');
}else {
    require(
        [
            'echarts',
            'echarts/chart/wordCloud'
        ],
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('label_left'));


            option = {
                title: {
                    // text: '关键词',
                },
                tooltip: {
                    show: true
                },
                series: [{
                    // name: 'Google Trends',
                    type: 'wordCloud',
                    size: ['80%', '80%'],
                    textRotation : [0, 0, 0, 0],
                    textPadding: 0,
                    autoSize: {
                        enable: true,
                        minSize: 14
                    },
                    data: user_key_series
                }]
            };

            myChart.setOption(option);
            var ecConfig = require('echarts/config');
            myChart.on(ecConfig.EVENT.HOVER, function (param){
                var selected = param.name;
            });
        }
    );
}

if (user_tag_series.length==0){
    $('#label_right').html('暂无数据');
}else {
    //----人物业务标签
    require(
        [
            'echarts',
            'echarts/chart/wordCloud'
        ],
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('label_right'));

            option = {
                title: {
                    // text: '微话题',
                },
                tooltip: {
                    show: true
                },
                series: [{
                    // name: 'Google Trends',
                    type: 'wordCloud',
                    size: ['80%', '80%'],
                    textRotation : [0, 0, 0, 0],
                    textPadding: 0,
                    autoSize: {
                        enable: true,
                        minSize: 14
                    },
                    data:user_tag_series
                }]
            };

            myChart.setOption(option);
            var ecConfig = require('echarts/config');
            myChart.on(ecConfig.EVENT.HOVER, function (param){
                var selected = param.name;
            });
        }
    );
}


