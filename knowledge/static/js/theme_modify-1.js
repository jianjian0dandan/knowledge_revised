//--标签
var tag_url='/theme/theme_analysis_basic/?theme_name='+theme_name
    +'&submit_user='+submit_user;
$.ajax({
    url:tag_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:tag
});
function tag(data) {
    var data=eval(data);
    if (data[0][4].length==0||data[0][4]==''||data[0][4]=='NULL'){
        $('#container .theme .tag .tags').html('暂无'+' <b class="add icon icon-plus"></b>');
        //添加
        $('.tags .add').on('click',function () {
            $('.add_tag').show();
            $('.t_sure').show();
        });
    }else {
        var tag='';
        for(var t=0;t<data[0][4].length;t++){
            if (data[0][4][t]==''){
                null;
            }else {
                tag+=' <span>'+data[0][4][t]+'</span> <b class="del icon icon-remove"></b>';
            }
        }
        tag+=' <b class="add icon icon-plus"></b>';
        $('#container .theme .tag .tags').html(tag);
        //删除
        $('.tags .del').on('click',function () {
            var k_label=$(this).prev().text();
            var del_or_add_url='/theme/theme_add_tag/?theme_name='+theme_name+'&submit_user='+submit_user+
                '&k_label='+k_label+'&operation=del';
            $.ajax({
                url: del_or_add_url,
                type: 'GET',
                dataType: 'json',
                async: true,
                success:del_or_add
            });
        });
        //添加
        $('.tags .add').on('click',function () {
            $('.add_tag').show();
            $('.t_sure').show();
        });
    }
}

//添加-----------标签
$('.t_sure').on('click',function () {
    var k_label=$('.add_tag').val();
    var del_or_add_url='/theme/theme_add_tag/?theme_name='+theme_name+'&submit_user='+submit_user+
        '&k_label='+k_label+'&operation=add';
    $.ajax({
        url: del_or_add_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:function (data) {
            if (data== true){
                alert('添加成功。');
                $.ajax({
                    url:tag_url,
                    type: 'GET',
                    dataType: 'json',
                    async: true,
                    success:tag
                });
            }else {
                alert('添加失败。');
            }
        }
    });
});

function del_or_add(data) {
    var data=eval(data);
    if (data== true){
        alert('删除成功。');
        $.ajax({
            url:tag_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:tag
        });
    }else {
        alert('删除失败。');
    }
};

//==============================================================================================

//关联资源
var source_url='/theme/show_theme_file/?theme_name='+theme_name
    +'&submit_user='+submit_user;
$.ajax({
    url:source_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:resources
});

function resources(data) {
    var data=eval(data);
    if (data.length==0||data==''||data=='NULL'){
        $('#container .theme .tag .source').html('暂无 <b class="s_add icon icon-plus"></b>');
        //添加
        $('.tag .s_add').on('click',function () {
            $('.add_resource').css({display:'inline-block'});
        });
    }else {
        var tag='';
        for(var t=0;t<data.length;t++){
            if (data[t][0]==''||data[t][1]==''){
                null;
            }else {
                tag+=' <a href="'+data[t][1]+'">'+data[t][0]+'</a> <b class="s_del icon icon-remove"></b>';
            }
        }
        tag+=' <b class="s_add icon icon-plus"></b>';
        $('#container .theme .tag .source').html(tag);
        //删除
        $('.s_del').on('click',function () {
            var label1=$(this).prev().text();
            var label2=$(this).prev().attr('href');
            var del_or_add_url='/theme/theme_edit_file/?theme_name='+theme_name+'&submit_user='+submit_user+
                '&operation=del'+'&file_name='+label1+','+label2;
            $.ajax({
                url: del_or_add_url,
                type: 'GET',
                dataType: 'json',
                async: true,
                success:del_or_add_resources
            });
        })
        //添加
        $('.tag .s_add').on('click',function () {
            $('.add_resource').css({display:'inline-block'});
        });
    }

};

function del_or_add_resources(data) {
    var data=eval(data);
    if (data== true){
        alert('删除成功。');
        $.ajax({
            url:source_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:resources
        });
    }else {
        alert('删除失败。');
    }
};
//添加---资源
$('.s_sure').on('click',function () {
    var label1=$('.add_source').val();
    var label2=$('.add_source_url').val();
    if (label1==''||label2==''){
        alert('请输入资源的名称或者链接，不能为空。');
    }else {
        var del_or_add_url='/theme/theme_edit_file/?theme_name='+theme_name+'&submit_user='+submit_user+
            '&operation=add'+'&file_name='+label1+','+label2;
        $.ajax({
            url: del_or_add_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:function (data) {
                if (data== true){
                    alert('添加成功。');
                    $.ajax({
                        url:source_url,
                        type: 'GET',
                        dataType: 'json',
                        async: true,
                        success:resources
                    });
                }else {
                    alert('添加失败。');
                }
            }
        });
    }
})

//=======================================================================================
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
                        var words=row[7];
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
                        var words=row[8];
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
        onCheckAll:function (row) {
            theme_diff.push(row[1]);
        },
        onUncheckAll:function (row) {
            theme_diff.removeByValue(row[1]);
        },
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='删除') {
                $('#fail').modal('show');
                event_id=row[0];
            }
        }
    });
};
var event_id;
function del() {
    var del_url='/theme/del_event_in_theme/?theme_name='+theme_name+'&submit_user='+submit_user+
        '&event_id='+event_id;
    $.ajax({
        url: del_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:function (data) {
            var data=eval(data);
            if (data== true){
                alert('删除成功。');
                $.ajax({
                    url: things_url,
                    type: 'GET',
                    dataType: 'json',
                    async: true,
                    success:things
                });
            }else {
                alert('删除失败。');
            }
        }
    });
}
//专题下----事件
var way='r';
function add_way(value) {
    if (value=='r'){
        way='r';
        $('.hands').hide();
        $('.event_list').css({display:'block'});
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
    }else {
        way='m';
        $('.event_list').css({display:'none'});
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
        $('.event_list').show();
    }
})

function event_list(data) {
    var data = eval(data);
    console.log(11)
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
                        var words=row[7];
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
                        var words=row[8];
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
            //多选框
            {
                title: "加入专题",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },

        ],
        onCheck:function (row) {
            thing_list.push(row[0]);
        },
        onUncheck:function (row) {
            thing_list.removeByValue(row[0]);
        },
        onCheckAll:function (row) {
            thing_list.push(row[1]);
        },
        onUncheckAll:function (row) {
            thing_list.removeByValue(row[1]);
        },
    });
};

var thing_list=[];
$('#add_theme').on('click',function () {
    var node_ids=thing_list.join(',');
    if(node_ids==''){
        alert('请检查您要加入的事件。(不能为空)')
    }else {
        var new_thing_url='/theme/create_relation/?node1_id='+node_ids+'&node2_id='+theme_name+
            '&submit_user='+submit_user;
        $.ajax({
            url:new_thing_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:new_thing
        });
    };
});

function new_thing(data) {
    if (data=='success'){
        alert('添加成功。');
        $.ajax({
            url: things_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:things
        });
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
        }else {
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
    }else if(data=='theme already exist') {
        alert('此事件已经存在，请检查您添加的事件。');
    }else {
        alert('添加失败。');
    }
}

//删除指定项
Array.prototype.removeByValue = function(val) {
    for(var i=0; i<this.length; i++) {
        if(this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
};