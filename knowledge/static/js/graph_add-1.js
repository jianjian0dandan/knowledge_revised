function type_1(value) {
    if (value==1){
        $('.user').show();
        $('.event').hide();
        $('.agency').hide();
    }else if (value==2) {
        $('.user').hide();
        $('.event').show();
        $('.agency').hide();
    }else if (value==3){
        $('.user').hide();
        $('.event').hide();
        $('.agency').show();
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
}

function type_3(value) {
    if (value==4){
        $('.user .manual-1').show();
        $('.user .manual').hide();
    }else if (value==5){
        $('.user .manual').show();
        $('.user .manual-1').hide();
    }
}

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
    }
}
//推荐人物
var recommend_url='';
$.ajax({
    url: recommend_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:recommend
});
function recommend(data) {
    var data = eval(data);
    $('#recommend').bootstrapTable('load', data);
    $('#recommend').bootstrapTable({
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