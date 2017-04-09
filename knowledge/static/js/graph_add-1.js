//推荐人物
var recommend_url='/construction/show_in/';
var uid=[];
$.ajax({
    url: recommend_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:recommend_1
});
function recommend_1(data1) {
    var data1 = eval(data1);
    uid=[];
    $('.recommend').css({display:'block'});
    $('.recommend2').css({display:'none'});
    $('.recommend3').css({display:'none'});
    $('.recommend4').css({display:'none'});
    $('#recommend').bootstrapTable('load', data1);
    $('#recommend').bootstrapTable({
        data:data1,
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
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "序号",//标题
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
                    return row[1];
                },
            },
            {
                title: "注册地",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==''){
                        return '未知';
                    }else {
                        return row[2];
                    }
                },
            },
            {
                title: "微博数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[3];
                },
            },
            {
                title: "粉丝数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[4];
                },
            },
            {
                title: '影响力',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[5].toFixed(2);
                },
            },
            //多选框
            {
                title: "",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },

        ],
        onCheck:function (row) {
            uid.push(row[0]);
        }
        // onClickRow: function (row, tr) {
        //     if ($(tr.context).index()==2) {
        //         del_eventuid=row[0];
        //         $('#del_ject').modal("show");
        //     }
        // }
    });
};

function recommend_2(data2) {
    var data2 = eval(data2);
    uid=[];
    $('.recommend').css({display:'none'});
    $('.recommend2').css({display:'block'});
    $('.recommend3').css({display:'none'});
    $('.recommend4').css({display:'none'});
    $('#recommend2').bootstrapTable('load', data2);
    $('#recommend2').bootstrapTable({
        data:data2,
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
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "序号",//标题
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
                    return row[1];
                },
            },
            {
                title: "注册地",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==''){
                        return '未知';
                    }else {
                        return row[2];
                    }
                },
            },
            {
                title: "粉丝数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[3];
                },
            },
            {
                title: "微博数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[4]
                },
            },
            {
                title: '敏感度',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if(row[5]==''){
                        return '未知';
                    }else {
                        return row[5].toFixed(2);
                    }
                },
            },
            {
                title: '敏感词',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if(row[6].length==0){
                        return '暂无';
                    }else {
                        $.each(row[6],function (index,item) {
                            return item;
                        })
                    }
                },
            },
            //多选框
            {
                title: "",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },

        ],
        onCheck:function (row) {
            uid.push(row[0]);
        }
        // onClickRow: function (row, tr) {
        //     if ($(tr.context).index()==2) {
        //         del_eventuid=row[0];
        //         $('#del_ject').modal("show");
        //     }
        // }
    });
};

function recommend_3(data3) {
    var data3 = eval(data3);
    uid=[];
    $('.recommend').css({display:'none'});
    $('.recommend2').css({display:'none'});
    $('.recommend3').css({display:'block'});
    $('.recommend4').css({display:'none'});
    $('#recommend3').bootstrapTable('load', data3);
    $('#recommend3').bootstrapTable({
        data:data3,
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
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "序号",//标题
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
                    return row[1];
                },
            },
            {
                title: "注册地",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==''){
                        return '未知';
                    }else {
                        return row[2];
                    }
                },
            },
            {
                title: "微博数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[3];
                },
            },
            {
                title: "粉丝数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[4]
                },
            },
            {
                title: '影响力',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[5].toFixed(2);
                },
            },
            {
                title: '关联用户',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[6];
                },
            },
            //多选框
            {
                title: "",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },

        ],
        onCheck:function (row) {
            uid.push(row[0]);
        }
        // onClickRow: function (row, tr) {
        //     if ($(tr.context).index()==2) {
        //         del_eventuid=row[0];
        //         $('#del_ject').modal("show");
        //     }
        // }
    });
};

function recommend_4(data4) {
    var data4 = eval(data4);
    uid=[];
    $('.recommend').css({display:'none'});
    $('.recommend2').css({display:'none'});
    $('.recommend3').css({display:'none'});
    $('.recommend4').css({display:'block'});
    $('#recommend4').bootstrapTable('load', data4);
    $('#recommend4').bootstrapTable({
        data:data4,
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
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "序号",//标题
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
                    return row[1];
                },
            },
            {
                title: "注册地",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==''){
                        return '未知';
                    }else {
                        return row[2];
                    }
                },
            },
            {
                title: "微博数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[3];
                },
            },
            {
                title: "粉丝数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[4];
                },
            },
            {
                title: '影响力',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[5].toFixed(2);
                },
            },
            //多选框
            {
                title: "",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },

        ],
        onCheck:function (row) {
            uid.push(row[0]);
        }
        // onClickRow: function (row, tr) {
        //     if ($(tr.context).index()==2) {
        //         del_eventuid=row[0];
        //         $('#del_ject').modal("show");
        //     }
        // }
    });
};

function recommend_5(data5) {
    var data5 = eval(data5);
    uid=[];
    $('.recommend').css({display:'none'});
    $('.recommend2').css({display:'none'});
    $('.recommend3').css({display:'none'});
    $('.recommend4').css({display:'none'});
    $('.recommend5').css({display:'block'});
    $('#recommend5').bootstrapTable('load', data5);
    $('#recommend5').bootstrapTable({
        data:data5,
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
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "序号",//标题
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
                    return row[1];
                },
            },
            {
                title: "注册地",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==''){
                        return '未知';
                    }else {
                        return row[2];
                    }
                },
            },
            {
                title: "微博数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[3];
                },
            },
            {
                title: "粉丝数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[4];
                },
            },
            {
                title: '影响力',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[5].toFixed(2);
                },
            },
            //多选框
            {
                title: "",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },

        ],
        onCheck:function (row) {
            uid.push(row[0]);
        }
        // onClickRow: function (row, tr) {
        //     if ($(tr.context).index()==2) {
        //         del_eventuid=row[0];
        //         $('#del_ject').modal("show");
        //     }
        // }
    });
};
//=======推荐人物==完=====


function type_1(value) {
    if (value==1){
        $('.user').show();
        $('.event').hide();
        $('.agency').hide();
        $('#node_list').show();
        $('#event_list').hide();
        node_type='user';
        type='influence';
        $('#node_list').css({display:'block'});
        $('#event_list').css({display:'none'});
        $('.count_task').css({display:'block'});
        $('.event_task').css({display:'none'});
    }else if (value==2) {
        $('.user').hide();
        $('.event').show();
        $('.agency').hide();
        $('#node_list').hide();
        $('#event_list').show();
        node_type='event';
        $('#node_list').css({display:'none'});
        $('#event_list').css({display:'block'});
        $('.count_task').css({display:'none'});
        $('.event_task').css({display:'block'});
    }else if (value==3){
        $('.user').hide();
        $('.event').hide();
        $('.agency').show();
        $('#node_list').show();
        $('#event_list').hide();
        node_type='org';
        type='influence';
        $('#node_list').css({display:'block'});
        $('#event_list').css({display:'none'});
        $('.count_task').css({display:'block'});
        $('.event_task').css({display:'none'});
    }
};

var recommendation_manual='r';
function type_2(value) {
    if (value==1){
        $('.user #tui_shou').empty();
        $('.user #tui_shou').append(
            '<option value="1">影响力推荐</option>'+
            '<option value="2">言论敏感度推荐</option>'+
            '<option value="3">关注用户推荐</option>'
        );
        recommendation_manual='r';
        $('.user .time_t').show();
        $('.user .manual-1').hide();
        $('.user .manual').hide();
    }else {
        $('.user #tui_shou').empty();
        $('.user #tui_shou').append(
            '<option value="4">文件导入</option>'+
            '<option value="5">手动添加</option>'
        );
        recommendation_manual='m';
        $('.user .time_t').hide();
        $('.user .manual-1').show();
        $('.user .manual').hide();
    }
};
//---7天时间
function get7DaysBefore(date,m){
    var date = date || new Date(),
        timestamp, newDate;
    if(!(date instanceof Date)){
        date = new Date(date);
    }
    timestamp = date.getTime();
    newDate = new Date(timestamp - m * 24 * 3600 * 1000);
    return [newDate.getFullYear(), newDate.getMonth() + 1, newDate.getDate()].join('-');
};
var day7=[];
for (var a=0;a < 8;a++){
    day7.push(get7DaysBefore(new Date(),a));
}
$('#task_time').empty();
for (var y=0;y<day7.length;y++){
    $('#task_time').append('<option value="'+day7[y]+'">'+day7[y]+'</option>');
}
$('#task_time_age').empty();
for (var y=0;y<day7.length;y++){
    $('#task_time_age').append('<option value="'+day7[y]+'">'+day7[y]+'</option>');
}
//---7天完

var recommend='影响力';
var type='influence';
var node_type='user';
var recommend_style='upload';
function type_3(value) {
    if (value==4){
        $('.user .manual-1').show();
        $('.user .manual').hide();
        recommend_style='upload';
    }else if (value==5){
        $('.user .manual').show();
        $('.user .manual-1').hide();
        recommend_style='write';
    }else if (value==1){
        recommend='影响力';
        type='influence';
    }else if (value==2){
        recommend='敏感度';
        type='sensitive';
    }else if (value==3){
        recommend='关注度';
        type='auto';
    }
};


//===========机构组织===============
function type_2_age(value) {
    if (value==1){
        $('.agency #tui_shou_age').empty();
        $('.agency #tui_shou_age').append(
            '<option value="1">影响力推荐</option>'+
            '<option value="2">言论敏感度推荐</option>'+
            '<option value="3">关注用户推荐</option>'
        );
        recommendation_manual='r';
        $('.agency .time_t_age').show();
        $('.agency .manual-1').hide();
        $('.agency .manual').hide();
    }else {
        $('.agency #tui_shou').empty();
        $('.agency #tui_shou').append(
            '<option value="4">文件导入</option>'+
            '<option value="5">手动添加</option>'
        );
        recommendation_manual='m';
        $('.agency .time_t_age').hide();
        $('.agency .manual-1').show();
        $('.agency .manual').hide();
    }
}

function type_3_age(value) {
    if (value==4){
        $('.agency .manual-1').show();
        $('.agency .manual').hide();
        recommend_style='upload';
    }else if (value==5){
        $('.agency .manual').show();
        $('.agency .manual-1').hide();
        recommend_style='write';
    }else if (value==1){
        recommend='影响力';
        type='influence';
    }else if (value==2){
        recommend='敏感度';
        type='sensitive';
    }else if (value==3){
        recommend='关注度';
        type='auto';
    }
}
//===========机构组织=========完======


//-----------推荐人物----------
$('.add_sure').on('click',function () {
    if (node_type=='event'){
        null;
    }else {
        var date='2016-11-27';
        // if (node_type=='user'){
        //     date=$('#task_time').val();
        // }else if (node_type=='org'){
        //     date=$('#task_time_age').val();
        // };
        var submit_user='admin';
        // var submit_user=$('#name').text();
        if (recommendation_manual=='r'){
            $('#recommend').empty();
            if (recommend=='关注度'){
                var recommend_url_3='/construction/show_auto_in/?date='+date+'&submit_user='+submit_user+
                    '&node_type='+node_type;
                $.ajax({
                    url: recommend_url_3,
                    type: 'GET',
                    dataType: 'json',
                    async: true,
                    success:recommend_3
                });
            }else if (recommend=='敏感度'){
                var recommend_url_2='/construction/show_in/?date='+date+'&type='+type+'&submit_user='+submit_user+
                    '&node_type='+node_type;
                $.ajax({
                    url: recommend_url_2,
                    type: 'GET',
                    dataType: 'json',
                    async: true,
                    success:recommend_2
                });
            }else {
                if (node_type=='org'){
                    var recommend_url_4='/construction/show_in/?date='+date+'&type='+type+'&submit_user='+submit_user+
                        '&node_type='+node_type;
                    $.ajax({
                        url: recommend_url_4,
                        type: 'GET',
                        dataType: 'json',
                        async: true,
                        success:recommend_4
                    });
                    task_renew();
                }else {
                    var recommend_url_5='/construction/show_in/?date='+date+'&type='+type+'&submit_user='+submit_user+
                        '&node_type='+node_type;
                    $.ajax({
                        url: recommend_url_5,
                        type: 'GET',
                        dataType: 'json',
                        async: true,
                        success:recommend_5
                    });
                }
            }
        }else if (recommendation_manual=='m'){
            calculate_rel();
        }
    }
})

//创建任务
function calculate_rel() {
    if (node_type=='user'){
        $('#relation .rel_list').empty();
        $('#relation .rel_list').append(
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="friend" checked> 交互'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="colleague" checked> 自述关联'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="colleague" checked> 业务关联'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="discuss" checked> 参与讨论'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="join" checked> 参与事件'+
            '</label>'
        );
    }else if (node_type=='event'){
        $('#relation .rel_list').empty();
        $('#relation .rel_list').append(
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="join" checked> 参与事件'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="discuss" checked> 参与讨论'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="contain" checked> 主题关联'+
            '</label>'
        )
    }else {
        $('#relation .rel_list').empty();
        $('#relation .rel_list').append(
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="friend" checked> 交互'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="colleague" checked> 业务关联'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="join" checked> 参与事件'+
            '</label>'+
            '<label class="checkbox-inline">'+
            '   <input type="checkbox" value="discuss" checked> 参与讨论'+
            '</label>'
        )
    }
    $('#relation').modal('show');
}
$('#container .node #node_list .node_join').on('click',function () {
    calculate_rel();
});

//文件上传
var updata_file;
function handleFileSelect(evt){
    var files = evt;
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var a = oFREvent.target.result;
            $.ajax({
                type:"POST",
                url:"/construction/read_file/",
                dataType: "json",
                async:false,
                data:{new_words:a},
                success: function(data){
                    if( data ){
                        updata_file=[];
                        var data=data;
                        updata_file=data;
                        window.setTimeout(function () {
                            alert('上传成功。');
                        },500);
                    }
                }
            });
        };
        reader.readAsText(f,'GB2312');
    }
};

function sure_task() {
    // var date=$('#task_time').val();
    var date='2016-11-27';
    var submit_user=$('#name').text();
    // var submit_user='admin';
    var status,user_rel=[];
    if($('#box1').is(':checked')) { status=1; };
    if($('#box2').is(':checked')) { status=2; };
    $("#relation .rel_list input:checkbox:checked").each(function (index,item) {
        user_rel.push($(this).val());
    });
    var user_rel_list=user_rel.join(',');
    var n_t=0;
    if(node_type=='user'){
        n_t=0;
    }else if(node_type=='org') {
        n_t=1;
    }
    if (recommendation_manual=='m'){
        var input_data,updata;
        if (recommend_style=='upload'){
            updata=updata_file;
        }else {
            updata=$('#container .node .attributes .manual .task_users').val().split(" ");
        }
        input_data={
            'date':date,'upload_data':updata,'node_type':n_t,'user':submit_user,'compute_status':status,
            'relation_string':user_rel_list,'recommend_style':recommend_style,'operation_type':'submit'
        };
        var group_url = '/construction/submit_identify_in/';
        $.ajax({
            type:'POST',
            url: group_url,
            contentType:"application/json",
            data: JSON.stringify(input_data),
            dataType: "json",
            success: fail_or_success
        });
    }else {
        var uid_list=uid.join(',');
        var new_task_url='/construction/admin_identify_in/?date='+date+'&uid_list='+uid_list+
            '&user_rel='+user_rel_list+'&status='+status+'&recommend_style='+type+
            '&node_type='+n_t+'&submit_user='+submit_user;
    }

    $.ajax({
        url: new_task_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:fail_or_success
    });
}
//创建成功与失败
function fail_or_success(data) {
    var data=eval(data);
    if (data.length>=0){
        if (data[0]==1){
            $('#fail_success #prompt').text('创建成功！'+'您成功创建'+data[3].length+'个节点。');
        }else {
            if (data[1]=='invalid user info'){
                $('#fail_success #prompt').text('创建失败,您输入的用户无效。');
            }else if (data[1]=='all user in'){
                $('#fail_success #prompt').text('创建失败,您输入的用户已经入库。');
            }
        }
    }else {
        if (data==1){
            $('#fail_success #prompt').text('创建成功');
        }else {
            $('#fail_success #prompt').text('创建失败');
        }
    }
    $('#fail_success').modal('show');
    task_renew();
}

//任务列表
function task_renew() {
    var nt;
    if(node_type=='user'){
        nt=0;
        $('.count_task').css({display:'block'});
        $('.count_task_2').css({display:'none'});
        var task_url='/construction/show_user_task_status/?node_type='+nt;
        $.ajax({
            url: task_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:task_list
        });
    }else if(node_type=='org') {
        nt=1;
        $('.count_task').css({display:'none'});
        $('.count_task_2').css({display:'block'});
        var task_url='/construction/show_user_task_status/?node_type='+nt;
        $.ajax({
            url: task_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:task_list_2
        });
    }

}
task_renew();
function task_list(data) {
    var data = eval(data);
    $('#count').bootstrapTable('load', data);
    $('#count').bootstrapTable({
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
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "人物名称",//标题
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
                title: "添加方式",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[6]=="influence"){
                        return '影响力推荐';
                    }else if(row[6]=="sensitive"){
                        return '敏感度推荐';
                    }else if(row[6]=="upload"){
                        return '上传文件';
                    }else if(row[6]=="write"){
                        return '手动输入';
                    }else if(row[6]=="auto"){
                        return '关注用户推荐';
                    }
                }
            },
            {
                title: "添加人",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[5];
                },
            },
            {
                title: "提交时间",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[1];
                },
            },
            {
                title: "任务状态",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==1){
                        return '立即计算';
                    }else if (row[2]==2){
                        return '预约计算';
                    }else if (row[2]==3){
                        return '正在计算';
                    }else if (row[2]==4){
                        return '计算完成';
                    }

                },
            },
            {
                title: "立即更新",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a>立即更新</a>';
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

function task_list_2(data) {
    var data = eval(data);
    $('#count_2').bootstrapTable('load', data);
    $('#count_2').bootstrapTable({
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
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "人物名称",//标题
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
                title: "添加方式",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[6]=="influence"){
                        return '影响力推荐';
                    }else if(row[6]=="sensitive"){
                        return '敏感度推荐';
                    }else if(row[6]=="upload"){
                        return '上传文件';
                    }else if(row[6]=="write"){
                        return '手动输入';
                    }else if(row[6]=="auto"){
                        return '关注用户推荐';
                    }
                }
            },
            {
                title: "添加人",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[5];
                },
            },
            {
                title: "提交时间",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row[1];
                },
            },
            {
                title: "任务状态",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[2]==1){
                        return '立即计算';
                    }else if (row[2]==2){
                        return '预约计算';
                    }else if (row[2]==3){
                        return '正在计算';
                    }else if (row[2]==4){
                        return '计算完成';
                    }

                },
            },
            {
                title: "立即更新",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a>立即更新</a>';
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



