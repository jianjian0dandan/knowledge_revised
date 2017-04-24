var _event_type={
    'military':'军事国防',
    'transport':'交通',
    'resources':'国土资源',
    'overseas':'境外敌对势力',
    'disaster':'灾害',
    'public_security':'社会公共安全',
    'rights':'维权上访',
    'information':'信息产业',
    'information_security':'信息安全',
    'industry':'工业',
    'network':'网络安全',
    'chinese_party':'中国共产党党务',
    'national':'国家政务',
    'diplomacy':'外交',
    'political':'政法监察',
    'comprehensive_group':'综合党团',
    'health':'卫生',
    'art_sports':'文化体育',
    'tourism':'旅游服务',
    'human_resources':'人力资源与社会保障',
    'population':'人口计生',
    'agriculture':'农业',
    'housing':'住房与城乡建设',
    'environment':'环境保护',
    'energy':'能源',
    'technology':'科技教育',
    'business':'商业贸易',
    'macro_economy':'宏观经济',
    'financial_work':'财政金融',
    'other':'其他'
};
function place() {
    //this.ajax_method='GET'; // body...
}
place.prototype= {
    call_request:function(url,callback) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:callback
        });
    },
};
var place=new place();
function nums() {
    var result_url='/relation/check_sim_nodes/?node_type='+node_type+'&node_id='+node_id+'&submit_user='+submit_user;
    place.call_request(result_url,result);
}
nums();


function result(data) {
    var data=eval(data);
    for (var key in data){
        //人物
        if (node_type=='User'){
            person(data[key]);
            $('.related_person').css({display:'block'});
        };
        //机构
        if (node_type=='Org'){
            agencies(data[key]);
            $('.related_agencies').css({display:'block'});
        };
        //事件
        if (node_type=='Event'){
            events(data[key]);
            $('.related_events').css({display:'block'});
        };
        //专题
        if (node_type=='SpecialEvent'){
            events(data[key]);
            $('.related_subject').css({display:'block'});
        };
        //群体
        if (node_type=='Group'){
            if (key == 'User'){
                person(data[key]);
                $('.related_person').css({display:'block'});
            }
            if (key == 'Org'){
                agencies(data[key]);
                $('.related_agencies').css({display:'block'});
            }
        };
    }
}
//相关人物
function person(data) {
    var data = eval(data);
    $('#person').bootstrapTable('load', data);
    $('#person').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40],//分页步进值
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
                    return row[1].uid;
                }
            },
            {
                title: "人物昵称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1].uname==''||row[1].uname=='unknown'||row[1].uname=='NULL'){
                        return row[1].uid;
                    }else {
                        return row[1].uname;
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
                    if (row[1].location==''||row[1].location=='unknown'||row[1].location=='NULL'){
                        return '未知';
                    }else {
                        return row[1].location;
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
                    if (row[1].influence==''||row[1].influence=='unknown'||row[1].influence=='NULL'){
                        return 0;
                    }else {
                        return row[1].influence.toFixed(2);
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
                    if (row[1].activeness==''||row[1].activeness=='unknown'||row[1].activeness=='NULL'){
                        return 0;
                    }else {
                        return row[1].activeness.toFixed(2);
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
                    if (row[1].sensitive==''||row[1].sensitive=='unknown'||row[1].sensitive=='NULL'){
                        return 0;
                    }else {
                        return row[1].sensitive.toFixed(2);
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
                    if (row[1].keywords_string==''||row[1].keywords_string=='unknown'||row[1].keywords_string=='NULL'){
                        return '暂无';
                    }else {
                        var words=row[1].keywords_string.split('&');
                        if (words.length<=5){
                            return words.join(',');
                        }else {
                            var key=words.splice(0,5).join(',');
                            var tit=words.splice(5).join(',');
                            return '<p title="'+tit+'">'+key+'</p> ';
                        }
                    }
                },
            },
            {
                title: "计算状态",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1].sim=='not exist'){
                        var infor=row[1].uname+','+row[1].uid+',User';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (row[1].sim==0){
                        return '尚未计算';
                    }else if (row[1].sim==1){
                        var name;
                        if (row[1].uname==''||row[1].uname=='unknown'||row[1].uname=='NULL'){
                            name= row[1].uid;
                        }else {
                            name= row[1].uname;
                        }
                        var go=row[1].uid+',User,'+name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (row[1].sim==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
            };
            if ($element[0].cellIndex==0){
                window.open('/index/person/?user_id='+row[1].id);
            }
        }
    });
};

//相关机构
function agencies(data) {
    var data = eval(data);
    $('#agencies').bootstrapTable('load', data);
    $('#agencies').bootstrapTable({
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
                title: "ID",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[1].id;
                }
            },
            {
                title: "机构名称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1].uname==''||row[1].uname=='unknown'||row[1].uname=='NULL'){
                        return row[1].id;
                    }else {
                        return row[1].uname;
                    }
                }
            },
            {
                title: "注册地",//标题
                field: "location",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1].location==''||row[1].location=='unknown'||row[1].location=='NULL'){
                        return '未知';
                    }else {
                        return row[1].location;
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
                    if (row[1].influence==''||row[1].influence=='unknown'||row[1].influence=='NULL'){
                        return 0;
                    }else {
                        return row[1].influence.toFixed(2);
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
                    if (row[1].activeness==''||row[1].activeness=='unknown'||row[1].activeness=='NULL'){
                        return 0;
                    }else {
                        return row[1].activeness.toFixed(2);
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
                    if (row[1].sensitive==''||row[1].sensitive=='unknown'||row[1].sensitive=='NULL'){
                        return 0;
                    }else {
                        return row[1].sensitive.toFixed(2);
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
                    if (row[1].keywords_string==''||row[1].keywords_string=='unknown'||row[1].keywords_string=='NULL'){
                        return '暂无';
                    }else {
                        var words=row[1].keywords_string.split('&');
                        if (words.length<=5){
                            return words.join(',');
                        }else {
                            var key=words.splice(0,5).join(',');
                            var tit=words.splice(5).join(',');
                            return '<p title="'+tit+'">'+key+'</p> ';
                        }
                    }
                },
            },
            {
                title: "计算状态",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1].sim=='not exist'){
                        var infor=row[1].uname+','+row[1].id+',Org';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (row[1].sim==0){
                        return '尚未计算';
                    }else if (row[1].sim==1){
                        var name;
                        if (row[1].uname==''||row[1].uname=='unknown'||row[1].uname=='NULL'){
                            name= row[1].id;
                        }else {
                            name= row[1].uname;
                        }
                        var go=row[1].uid+',Org,'+name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (row[1].sim==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
            };
            if ($element[0].cellIndex==0){
                window.open('/index/organization/?user_id='+row[1].id);
            }
        }
    });
};

//相关事件
function events(data) {
    var data = eval(data);
    $('#events').bootstrapTable('load', data);
    $('#events').bootstrapTable({
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
                    if (row[1].name==''||row[1].name=='unknown'||row[1].name=='NULL'){
                        return '暂无';
                    }else {
                        return row[1].name;
                    }
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
                    if (row[1].event_type==''||row[1].event_type=='unknown'||row[1].event_type=='NULL'){
                        return '暂无';
                    } else {
                        return _event_type[row[1].event_type];
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
                    if (row[1].real_time==''||row[1].real_time=='unknown'||row[1].real_time=='NULL'){
                        return '暂无';
                    }else {
                        return row[1].real_time;
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
                    if (row[1].real_geo==''||row[1].real_geo=='unknown'||row[1].real_geo=='NULL'){
                        return '暂无';
                    }else {
                        return row[1].real_geo;
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
                    if (row[1].uid_counts==''||row[1].uid_counts=='unknown'||row[1].uid_counts=='NULL'){
                        return 0;
                    }else {
                        return row[1].uid_counts;
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
                    if (row[1].weibo_counts==''||row[1].weibo_counts=='unknown'||row[1].weibo_counts=='NULL'){
                        return 0;
                    }else {
                        return row[1].weibo_counts;
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
                    if (row[1].keywords==''||row[1].keywords=='unknown'||row[1].keywords=='NULL'){
                        return '暂无';
                    }else {
                        var words=row[1].keywords.split('&');
                        if (words.length<=5){
                            return words.join(',');
                        }else {
                            var key=words.splice(0,5).join(',');
                            var tit=words.splice(5).join(',');
                            return '<p title="'+tit+'">'+key+'</p> ';
                        }
                    }
                },
            },
            {
                title: "计算状态",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[1].sim=='not exist'){
                        var infor=row[1].name+','+row[1].id+',Event';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (row[1].sim==0){
                        return '尚未计算';
                    }else if (row[1].sim==1){
                        var go=row[1].uid+',Event,'+row[1].name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (row[1].sim==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
            };
            if ($element[0].cellIndex==0){
                window.open('/index/event/?user_id='+row[1].id);
            }
        }
    });
};

//相关专题
// function subject(data) {
//     var data = eval(data);
//     $('#subject').bootstrapTable('load', data);
//     $('#subject').bootstrapTable({
//         data:data,
//         search: true,//是否搜索
//         pagination: true,//是否分页
//         pageSize: 5,//单页记录数
//         pageList: [5, 20, 40, 80],//分页步进值
//         sidePagination: "client",//服务端分页
//         searchAlign: "left",
//         searchOnEnterKey: false,//回车搜索
//         showRefresh: true,//刷新按钮
//         showColumns: true,//列选择按钮
//         buttonsAlign: "right",//按钮对齐方式
//         locale: "zh-CN",//中文支持
//         detailView: false,
//         showToggle:true,
//         sortName:'bci',
//         sortOrder:"desc",
//         columns: [
//             {
//                 title: "专题名称",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//                     return index+1;
//                 }
//             },
//             {
//                 title: "关键词",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 }
//             },
//             {
//                 title: "业务标签",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//             {
//                 title: "包含事件数量",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//             {
//                 title: "创建时间",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//             {
//                 title: "相似度",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//         ],
//         // onClickRow: function (row, tr) {
//         //     if ($(tr.context).index()==2) {
//         //         del_eventuid=row[0];
//         //         $('#del_ject').modal("show");
//         //     }
//         // }
//     });
// };

//相关组织
// function organization(data) {
//     var data = eval(data);
//     $('#organization').bootstrapTable('load', data);
//     $('#organization').bootstrapTable({
//         data:data,
//         search: true,//是否搜索
//         pagination: true,//是否分页
//         pageSize: 5,//单页记录数
//         pageList: [5, 20, 40, 80],//分页步进值
//         sidePagination: "client",//服务端分页
//         searchAlign: "left",
//         searchOnEnterKey: false,//回车搜索
//         showRefresh: true,//刷新按钮
//         showColumns: true,//列选择按钮
//         buttonsAlign: "right",//按钮对齐方式
//         locale: "zh-CN",//中文支持
//         detailView: false,
//         showToggle:true,
//         sortName:'bci',
//         sortOrder:"desc",
//         columns: [
//             {
//                 title: "组织名称",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//                     return index+1;
//                 }
//             },
//             {
//                 title: "关键词",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 }
//             },
//             {
//                 title: "业务标签",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//             {
//                 title: "参与人数",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//             {
//                 title: "创建时间",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//             {
//                 title: "相似节点",//标题
//                 field: "",//键名
//                 sortable: true,//是否可排序
//                 order: "desc",//默认排序方式
//                 align: "center",//水平
//                 valign: "middle",//垂直
//                 formatter: function (value, row, index) {
//
//                 },
//             },
//         ],
//         // onClickRow: function (row, tr) {
//         //     if ($(tr.context).index()==2) {
//         //         del_eventuid=row[0];
//         //         $('#del_ject').modal("show");
//         //     }
//         // }
//     });
// };

function add_new_task(row) {
    var information=row.split(',');
    var time=Date.parse(new Date());
    var creat_url='/relation/compute_sim/?submit_user='+submit_user+'&submit_ts='+time+
        '&node_name='+information[0]+'&node_id='+information[1]+'&node_type='+information[2];
    $.ajax({
        url: creat_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:function (data) {
            if (data == 'yes'){
                alert('创建成功。');
                nums();
            }else {
                alert('创建失败。');
            }
        },
    });
}

function go_jump(uid_type) {
    var news=uid_type.split(',');
    window.open('/relation/similarity_result/?node_id='+news[0]+'&node_type='+news[1]+'&name='+news[2]);
}



