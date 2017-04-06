//标签
var tag_url='/theme/theme_analysis_basic/?theme_name='+theme_name
    +'&submit_user='+submit_user;
$.ajax({
    url:tag_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:function (data) {
        var data=eval(data);
        console.log(data)
        if (data[0][4].length==0||data[0][4]==''||data[0][4]=='NULL'){
            $('#container .theme .tag .tags').html('暂无');
        }else {
            var tag='';
            for(var t=0;t<data[0][4].length;t++){
                tag+='<span>'+data[0][4][t]+'</span> <b class="del icon icon-remove"></b>';
            }
            tag+=' <b class="add icon icon-plus"></b>';
            $('#container .theme .tag .tags').html(tag);
        }
        $('.del').on('click',function () {
            var k_label=$(this).text();
            var del_or_add_url='/theme/theme_add_tag/?theme_name='+theme_name+'&submit_user='+submit_user+
                    '&k_label='+k_label+'&operation=del';
            $.ajax({
                url: del_or_add_url,
                type: 'GET',
                dataType: 'json',
                async: true,
                success:del_or_add
            });
        })
    }
});
function del_or_add(data) {
    var data=eval(data);
}


//专题下的事件
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
    $('#theme_list').bootstrapTable('load', data);
    $('#theme_list').bootstrapTable({
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
                    if (row[2]==''||row[2]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[3]==''||row[3]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[4]==''||row[4]=='NULL'){
                        return '未知';
                    }else{
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
                    if (row[5]==''||row[5]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[6]==''||row[6]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[7].length==0||row[7]==''||row[7]=='NULL'){
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
                    if (row[8].length==0||row[8]==''||row[8]=='NULL'){
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
            {
                title: "删除",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '删除';
                },
            },
            //多选框
            // {
            //     title: "专题对比",//标题
            //     field: "select",
            //     checkbox: true,
            //     align: "center",//水平
            //     valign: "middle"//垂直
            // },

        ],
        onCheck:function (row) {
            theme_diff.push(row[1]);
        },
        onUncheck:function (row) {
            theme_diff.removeByValue(row[1]);
        },
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='查看专题') {
                window.open('/theme/result/?theme_name='+row[1]);
            }else if ($element[0].innerText=='编辑专题') {
                // window.open(+row[1]);
            }
        }
    });
};

//专题下----事件
var way='r';
function add_way(value) {
    if (value=='r'){
        way='r';
        $('.hands').hide();
    }else {
        way='m';
        $('.hands').show();
    }
};

if (way=='r') {
    // 专题下--------关联添加
    var event_list_url='/theme/search_related_event/?theme_name='+theme_name
        +'&submit_user='+submit_user;
    $.ajax({
        url:event_list_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:event_list
    });
}

$('#container .event .event-1 .sure').on('click',function () {
    if (way=='m'){
        var item=$('#name_or_word').val();
        // 专题下--------手动添加
        var search_event_url='/theme/search_related_event_item/?theme_name='+theme_name+'&item='+item
            +'&submit_user='+submit_user;
        $.ajax({
            url:search_event_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:event_list
        });
    }
})

function event_list(data) {
    var data = eval(data);
    $('#event_list').bootstrapTable('load', data);
    $('#event_list').bootstrapTable({
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
                    if (row[2]==''||row[2]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[3]==''||row[3]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[4]==''||row[4]=='NULL'){
                        return '未知';
                    }else{
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
                    if (row[5]==''||row[5]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[6]==''||row[6]=='NULL'){
                        return '暂无';
                    }else{
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
                    if (row[7].length==0||row[7]==''||row[7]=='NULL'){
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
                    if (row[8].length==0||row[8]==''||row[8]=='NULL'){
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
            {
                title: "删除",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '删除';
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

        },
        onUncheck:function (row) {

        },
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='查看专题') {

            }else if ($element[0].innerText=='编辑专题') {

            }
        }
    });
};



//删除指定项
Array.prototype.removeByValue = function(val) {
    for(var i=0; i<this.length; i++) {
        if(this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
};