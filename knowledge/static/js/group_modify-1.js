//--标签
var tag_url='/group/group_basic/?g_name='+theme_name +'&submit_user='+submit_user;
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
            var del_or_add_url='/group/group_add_tag/?g_name='+theme_name+'&submit_user='+submit_user+
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
    var del_or_add_url='/group/group_add_tag/?g_name='+theme_name+'&submit_user='+submit_user+
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
var source_url='/group/group_file_link/?g_name='+theme_name
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
            var del_or_add_url='/group/group_edit_file/?g_name='+theme_name+'&submit_user='+submit_user+
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
        var del_or_add_url='/group/group_edit_file/?g_name='+theme_name+'&submit_user='+submit_user+
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

//群体下的人物
var things_url='/group/group_detail/?g_name='+theme_name+'&submit_user='+submit_user;
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
        showToggle:false,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "人物ID",//标题
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
                    if (row[1]==''||row[1]=='NULL'){
                        return row[0];
                    }else{
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
                    }else{
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
                    }else{
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
                    if (row[4]==''||row[4]=='NULL'){
                        return 0;
                    }else{
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
                    }else{
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
                    if (row[6].length==0||row[6]==''||row[6]=='NULL'||row[6]=='null'){
                        return '暂无';
                    }else {
                        var words=row[6].split('&');
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
                    if (row[7].length==0||row[7]==''||row[7]=='NULL'){
                        return '暂无';
                    }else {
                        var words=row[7].split('&');
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
                    return '<a style="cursor: pointer;">删除</a>';
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
    var del_url='/group/del_user_in_group/?g_name='+theme_name+'&submit_user='+submit_user+
        '&uid='+event_id;
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
//群体下----人物
var way='r';
function add_way(value) {
    thing_list=[];
    if (value=='r'){
        way='r';
        $('.hands').hide();
        // 群体下--------关联添加
        var event_list_url='/group/search_related_people_auto/?g_name='+theme_name
            +'&submit_user='+submit_user;
        $.ajax({
            url:event_list_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:event_list
        });
        $('.event_list').css({display:'block'});
    }else {
        way='m';
        $('.event_list').css({display:'none'});
        $('.hands').show();
    }
};

if (way=='r') {
    // 群体下--------关联添加
    var event_list_url='/group/search_related_people_auto/?g_name='+theme_name
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
        var search_event_url='/group/search_related_people_item/?g_name='+theme_name+'&item='+item
            +'&submit_user='+submit_user;
        $.ajax({
            url:search_event_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:event_list
        });
        $('.event_list').css({display:'block'});
    }
});

function event_list(data) {
    console.log(data)
    if (data.length==0){
        null;
    }else {
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
            showToggle:false,
            sortName:'bci',
            sortOrder:"desc",
            columns: [
                {
                    title: "人物ID",//标题
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
                        if (row[1]==''||row[1]=='NULL'){
                            return row[0];
                        }else{
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
                        }else{
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
                        }else{
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
                        if (row[4]==''||row[4]=='NULL'){
                            return 0;
                        }else{
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
                        }else{
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
                        if (row[6].length==0||row[6]==''||row[6]=='NULL'){
                            return '暂无';
                        }else {
                            var words=row[6].split('&');
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
                        if (row[7].length==0||row[7]==''||row[7]=='NULL'){
                            return '暂无';
                        }else {
                            var words=row[7].split('&');
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
                    title: "加入群体",//标题
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
                thing_list.push(row[0]);
            },
            onUncheckAll:function (row) {
                thing_list.removeByValue(row[0]);
            },
        });
    };
};

var thing_list=[];
$('#add_theme').on('click',function () {
    var node_ids=thing_list.join(',');
    if(node_ids==''){
        alert('请检查您要加入的群体。(不能为空)')
    }else {
        var new_thing_url='/group/create_new_relation/?node1_id='+node_ids+'&node2_id='+theme_name+
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
    if (data==1){
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
            var event_list_url='/group/search_related_people_item/?g_name='+theme_name
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
            var search_event_url='/group/search_related_people_item/?g_name='+theme_name+'&item='+item
                +'&submit_user='+submit_user;
            $.ajax({
                url:search_event_url,
                type: 'GET',
                dataType: 'json',
                async: true,
                success:event_list
            });
        }
    }else if(data=='group already exist') {
        alert('人物已经存在，请检查您添加的人物。');
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