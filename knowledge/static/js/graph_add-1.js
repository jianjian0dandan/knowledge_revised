//推荐人物
var recommend_url='/construction/show_in/';
$.ajax({
    url: recommend_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:recommend_1
});
function recommend_1(data1) {
    var data1 = eval(data1);
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
    $('#recommend').bootstrapTable('load', data2);
    $('#recommend').bootstrapTable({
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
                    if(row[6]==''){
                        return '暂无';
                    }else {
                        return row[6];
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
    $('#recommend').bootstrapTable('load', data3);
    $('#recommend').bootstrapTable({
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
    }else if (value==2) {
        $('.user').hide();
        $('.event').show();
        $('.agency').hide();
        $('#node_list').hide();
        $('#event_list').show();
    }else if (value==3){
        $('.user').hide();
        $('.event').hide();
        $('.agency').show();
        $('#node_list').show();
        $('#event_list').hide();
        node_type='org';
        type='influence';
    }
};

function type_2(value) {
    if (value==1){
        $('.user #tui_shou').empty();
        $('.user #tui_shou').append(
            '<option value="1">影响力推荐</option>'+
            '<option value="2">言论敏感度推荐</option>'+
            '<option value="3">关注用户推荐</option>'
        );
        $('.user .time_t').show();
        $('.user .manual-1').hide();
        $('.user .manual').hide();
    }else {
        $('.user #tui_shou').empty();
        $('.user #tui_shou').append(
            '<option value="4">文件导入</option>'+
            '<option value="5">手动添加</option>'
        );
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
function type_3(value) {
    if (value==4){
        $('.user .manual-1').show();
        $('.user .manual').hide();
    }else if (value==5){
        $('.user .manual').show();
        $('.user .manual-1').hide();
    }else if (value==1){
        recommend='影响力';
        type='influence';
    }else if (value==2){
        recommend='敏感度';
        type='sensitive';
    }else if (value==3){
        recommend='关注度';
    }
};

function event_type_2(value) {
    if(value==2){
        $('.event .manual').show();
        $('.event .manual-1').show();
        $('.event .manual-2').hide();
    }else if (value==3){
        $('.event .manual').hide();
        $('.event .manual-1').hide();
        $('.event .manual-2').show();
    }else {
        $('.event .manual').hide();
        $('.event .manual-1').hide();
        $('.event .manual-2').hide();
    }
}

function type_2_age(value) {
    if (value==1){
        $('.agency #tui_shou_age').empty();
        $('.agency #tui_shou_age').append(
            '<option value="1">影响力推荐</option>'+
            '<option value="2">言论敏感度推荐</option>'+
            '<option value="3">关注用户推荐</option>'
        );
    }else {
        $('.agency #tui_shou_age').empty();
        $('.agency #tui_shou_age').append(
            '<option value="4">文件导入</option>'+
            '<option value="5">手动添加</option>'
        );
        $('.agency .time_t_age').hide();
        $('.agency .manual-1').show();
        $('.agency .manual').hide();
    }
}

function type_3_age(value) {
    if (value==4){
        $('.agency .manual-1').show();
        $('.agency .manual').hide();
    }else if (value==5){
        $('.agency .manual').show();
        $('.agency .manual-1').hide();
    }else if (value==1){
        recommend='影响力';
        type='influence';
    }else if (value==2){
        recommend='敏感度';
        type='sensitive';
    }else if (value==3){
        recommend='关注度';
    }
}

//-----------推荐人物下----------
$('.add_sure').on('click',function () {
    $('#recommend').empty();
    // var date=$('#task_time').val();
    var date='2016-11-27';
    // var submit_user=$('#name').text();
    var submit_user='admin';
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
        var recommend_url_1='/construction/show_in/?date='+date+'&type='+type+'&submit_user='+submit_user+
            '&node_type='+node_type;
        $.ajax({
            url: recommend_url_1,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:recommend_1
        });
    }
})


