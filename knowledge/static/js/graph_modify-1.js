//节点编辑
var node_type='User';
function type_node(value) {
    node_type=value;
}
$('#container .attributes .submit').on('click',function () {
    var item=$('#container .attributes .node_name').val();
    if (item==''){
        alert('请输入节点。(不能为空)');
    }else {
        var node_url='/construction/node_edit_search/?item='+item+'&node_type='+node_type+
            '&submit_user='+submit_user;
        // var node_url='/construction/node_edit_search/?item='+item+'&node_type='+node_type+
        //     '&submit_user='+submit_user+'&start_ts='+'&end_ts=';
        if (node_type=='Event'){
            $('.node_list').hide();
            $('.event_list').show();
            $.ajax({
                url: node_url,
                type: 'GET',
                dataType: 'json',
                async: true,
                success:event
            });
        }else {
            $('.node_list').show();
            $('.event_list').hide();
            $.ajax({
                url: node_url,
                type: 'GET',
                dataType: 'json',
                async: true,
                success:node
            });
        }

    }
})

function node(data) {
    var data = eval(data);
    $('#node_list').bootstrapTable('load', data);
    $('#node_list').bootstrapTable({
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
            // {
            //     title: "序号",//标题
            //     field: "",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         return index+1;
            //     }
            // },
            {
                title: "用户ID",//标题
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
                    if (row[6]==''||row[6]=='unknown'||row[6]=='NULL'){
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
                    if (row[7]==''||row[7]=='unknown'||row[7]=='NULL'){
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
                title: "编辑",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a>立即更新</a><br/>' +
                        '<a type="button" data-toggle="modal" data-target="#complie" onclick="go('+row[0]+')">编辑</a><br/>' +
                        '<a>删除</a>';
                },
            },

            // //多选框
            // {
            //     title: "",//标题
            //     field: "select",
            //     checkbox: true,
            //     align: "center",//水平
            //     valign: "middle"//垂直
            // },

        ],
        onClickCell: function (field, value, row, $element) {

        }
    });
};

function go(item) {
    item=item;
    $('.group-1').css({display:'none'});
    $('.tags-1').css({display:'none'});
    $('.words-1').css({display:'none'});
    $('.group-1 input').val("");
    $('.tags-1 input').val("");
    $('.words-1 input').val("");
    var com_url='/construction/node_edit_show/?node_type='+node_type+'&item='+item+
        '&submit_user='+submit_user;
    $.ajax({
        url: com_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:com
    });
}

function com(data) {
    var data=eval(data);
    console.log(data)
    $('#complie #tags').empty();
    $('#complie #words').empty();
    $('#complie #group').empty();
    var name;
    if (data[1]==''||data[1]=='NULL'||data[1]=='unknown'){
        name=data[0];
    }else {
        name=data[1];
    };
    $('#complie .name').text(name);
    if (data[2]==''||data[2]=='NULL'||data[2]=='unknown'){
        $('#complie #ID-1').val('');
    }else {
        $('#complie #ID-1').val(data[2]);
    };
    if (data[3]==''||data[3]=='NULL'||data[3]=='unknown'){
        null;
    }else {
        var topic=$('#topic [name=rels]:checkbox');
        var top=data[3].split('&');
        for(var i=0;i<topic.length;i++){
            //当前checkbox实现勾选
            for (var j=0;j<top.length;j++){
                if (topic[i].value==top[j]){
                    topic[i].checked=true;
                }
            }
        }
    };
    if (data[4]==''||data[4]=='NULL'||data[4]=='unknown'){
        $('#complie #business #business-1').val('暂无');
    }else {
        $('#complie #business #business-1').val(data[4]);
    };
    if (data[5]==''||data[5]=='NULL'||data[5]=='unknown'||data[5].length==0){
        $('#complie #tags').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var tag='';
        for(var t=0;t<data[5].length;t++){
            tag+=' <a>'+data[5][t]+'</a> <b class="del icon icon-remove"></b>';
        }
        tag+=' <b class="add icon icon-plus"></b>';
        $('#complie #tags').append(tag);
    };

    if (data[6]==''||data[6]=='NULL'||data[6]=='unknown'||data[6].length==0){
        $('#complie #words').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var doc=data[6];
        var tag='';
        for(var t=0;t<doc.length;t++){
            var a=doc[t].split(',');
            tag+=' <a href="'+a[1]+'">'+a[0]+'</a> <b class="del icon icon-remove"></b>';
        }
        tag+=' <b class="add icon icon-plus"></b>';
        $('#complie #words').append(tag);
    };
    if (data[7]==''||data[7]=='NULL'||data[7]=='unknown'||data[7].length==0){
        $('#complie #group').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var tag='';
        for(var t=0;t<data[7].length;t++){
            tag+=' <a>'+data[7][t]+'</a> <b class="del icon icon-remove"></b>';
        }
        tag+=' <b class="add icon icon-plus"></b>';
        $('#complie #group').append(tag);
    };

    $('.add').on('click',function () {
        $(this).parent().next().css({display:'block'});
        words=$(this).parent().next().attr('class');
    });
    $('.del').on('click',function () {
        $(this).prev().remove('a');
        $(this).remove();
    });
};
var words;
var documents;
var related_docs='';
var event_related_docs='';

$('.btn-xs').on('click',function () {
    if (words=='words-1'){
        var _tit=$(this).prevAll('.tit').val();
        var _url=$(this).prevAll('.url').val();
        if (_tit==''||_url==''){
            alert('不能为空。');
        }else {
            if (related_docs==''){
                related_docs+=_tit+','+_url;
            }else {
                related_docs+='+'+_tit+','+_url;
            }
            $(this).parent().prev().find('span').remove();
            $(this).parent().prev().find('.add').before(
                ' <a href="'+_url+'">'+_tit+'</a> <b class="s_del icon icon-remove"></b> '
            );
        }
    }else if (documents=='documents-1'){
        var _tit=$(this).prevAll('.e_tit').val();
        var _url=$(this).prevAll('.e_url').val();
        if (_tit==''||_url==''){
            alert('不能为空。');
        }else {
            if (event_related_docs==''){
                event_related_docs+=_tit+','+_url;
            }else {
                event_related_docs+='+'+_tit+','+_url;
            }
            $(this).parent().prev().find('span').remove();
            $(this).parent().prev().find('.add').before(
                ' <a href="'+_url+'">'+_tit+'</a> <b class="s_del icon icon-remove"></b> '
            );
        }
    } else {
        var _new=$(this).prev().val();
        if (_new==''){
            alert('不能为空。');
        }else {
            $(this).parent().prev().find('span').remove();
            $(this).parent().prev().find('.add').before('<a>'+_new+'</a> <b class="del icon icon-remove"> ');
        }
    }
});

//事件
function event(data) {
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
        showRefresh: true,//刷新按钮
        showColumns: true,//列选择按钮
        buttonsAlign: "right",//按钮对齐方式
        locale: "zh-CN",//中文支持
        detailView: false,
        showToggle:true,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            // {
            //     title: "序号",//标题
            //     field: "",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         return index+1;
            //     }
            // },
            {
                title: "事件名称",//标题
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
                },
            },
            {
                title: "入库时间",//标题
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
                    if (row[7]==''||row[7]=='unknown'||row[7]=='NULL'){
                        return '暂无';
                    }else {
                        if (row[7].length<=5){
                            return row[7].join(',');
                        }else {
                            var words=row[7].splice(0,5).join(',');
                            var tit=row[7].splice(5).join(',');
                            return '<p title="'+tit+'">'+words+'</p> ';
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
                    if (row[8]==''||row[8]=='unknown'||row[8]=='NULL'){
                        return '暂无';
                    }else {
                        if (row[8].length<=5){
                            return row[8].join(',');
                        }else {
                            var words=row[8].splice(0,5).join(',');
                            var tit=row[8].splice(5).join(',');
                            return '<p title="'+tit+'">'+words+'</p> ';
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
                    if (row[9] < 0){
                        return '正在计算';
                    }else if (row[9]= 1){
                        return '计算完成';
                    }else if (row[9]= 0){
                        return '尚未计算';
                    }
                },
            },
            {
                title: "操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a>立即更新</a><br/>' +
                        '<a onclick="run(\''+row[0]+'\')">编辑</a><br/>' +

                        // '<a onclick="run(\''+row[0]+'\')">编辑</a><br/>' +
                        '<a>删除</a>';
                },
            },
            // //多选框
            // {
            //     title: "",//标题
            //     field: "select",
            //     checkbox: true,
            //     align: "center",//水平
            //     valign: "middle"//垂直
            // },

        ],
        onClickCell: function (field, value, row, $element) {

        }
    });
};

function run(item) {
    e_item=item;
    $('.person-1').css({display:'none'});
    $('.org-1').css({display:'none'});
    $('.e_tag-1').css({display:'none'});
    $('.documents-1').css({display:'none'});
    $('.documents-1').css({display:'none'});
    $('.special-1').css({display:'none'});
    $('.person-1 input').val("");
    $('.org-1 input').val("");
    $('.e_tag-1 input').val("");
    $('.documents-1 input').val("");
    $('.special-1 input').val("");
    var event_com_url='/construction/node_edit_show/?node_type='+node_type+'&item='+item+
        '&submit_user='+submit_user;
    $.ajax({
        url: event_com_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:event_com
    });
};
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日|上午|下午/g, " ");
}
function event_com(data) {
    var data=eval(data);
    console.log(data)
    $('#event_complie .counts').empty();
    $('#event_complie #person').empty();
    $('#event_complie #special').empty();
    $('#event_complie #e_tag').empty();
    $('#event_complie #documents').empty();
    //名字
    var name;
    if (data[1]==''||data[1]=='NULL'||data[1]=='unknown'){
        name=data[0];
    }else {
        name=data[1];
    };
    $('#event_complie .name').text(name);
    //地点
    if (data[2]==''||data[2]=='NULL'||data[2]=='unknown'){
        $('#event_complie #place').val('未知');
    }else {
        $('#event_complie #place').val(data[2]);
    };
    //发生时间
    if (data[3]==''||data[3]=='NULL'||data[3]=='unknown'){
        $('#event_complie .time').val('');
    }else {
        $('#event_complie .time').val(getLocalTime(data[3]));
    };
    //事件类型
    if (data[4]==''||data[4]=='NULL'||data[4]=='unknown'){
        $('#event_complie #event_type-1').val('');
    }else {
        $('#event_complie #event_type-1').val(data[4]);
    };
    //关注周期
    if (data[5]==''||data[5]=='NULL'||data[5]=='unknown'){
        $('#event_complie .start').val('');
    }else {
        $('#event_complie .start').val(getLocalTime(data[5]));
    };

    if (data[6]==''||data[6]=='NULL'||data[6]=='unknown'){
        $('#event_complie .end').val('');
    }else {
        $('#event_complie .end').val(getLocalTime(data[6]));
    };
    //实际参与人物
    if (data[7]==''||data[7]=='NULL'||data[7]=='unknown'||data[7].length==0){
        $('#event_complie #person').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var tag=data[7].split('&');
        var user='';
        for(var t=0;t<tag.length;t++){
            user+=' <a>'+tag[t]+'</a> <b class="del icon icon-remove"></b>';
        }
        user+=' <b class="add icon icon-plus"></b>';
        $('#event_complie #person').append(user);
    };
    //实际参与机构
    if (data[8]==''||data[8]=='NULL'||data[8]=='unknown'||data[8].length==0){
        $('#event_complie #org').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var tag=data[8].split('&');
        var org='';
        for(var t=0;t<tag.length;t++){
            org+=' <a>'+tag[t]+'</a> <b class="del icon icon-remove"></b>';
        }
        org+=' <b class="add icon icon-plus"></b>';
        $('#event_complie #org').append(org);
    };
    //所属专题
    if (data[12]==''||data[12]=='NULL'||data[12]=='unknown'||data[12].length==0){
        $('#event_complie #special').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var tag='';
        for(var t=0;t<data[12].length;t++){
            tag+=' <a>'+data[12][t]+'</a> <b class="del icon icon-remove"></b>';
        }
        tag+=' <b class="add icon icon-plus"></b>';
        $('#event_complie #special').append(tag);
    };
    //业务标签
    if (data[9]==''||data[9]=='NULL'||data[9]=='unknown'||data[9].length==0){
        $('#event_complie #e_tag').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var tag='';
        for(var t=0;t<data[9].length;t++){
            tag+=' <a>'+data[9][t]+'</a> <b class="del icon icon-remove"></b>';
        }
        tag+=' <b class="add icon icon-plus"></b>';
        $('#event_complie #e_tag').append(tag);
    };
    //关联文档
    if (data[11]==''||data[11]=='NULL'||data[11]=='unknown'||data[11].length==0){
        $('#event_complie #documents').append('<span>暂无</span>'+' <b class="add icon icon-plus"></b>');
    }else {
        var doc=data[11];
        var tag='';
        for(var t=0;t<doc.length;t++){
            var a=doc[t].split(',');
            tag+=' <a href="'+a[1]+'">'+a[0]+'</a> <b class="del icon icon-remove"></b>';
        }
        tag+=' <b class="add icon icon-plus"></b>';
        $('#event_complie #documents').append(tag);
    };
    //事件描述
    if (data[10]==''||data[10]=='NULL'||data[10]=='unknown'){
        $('#event_complie #e_business #e_business-1').val('暂无');
    }else {
        $('#event_complie #e_business #e_business-1').val(data[10]);
    };
    $('#event_complie').modal('show');
    $('.add').on('click',function () {
        $(this).parent().next().css({display:'block'});
        documents=$(this).parent().next().attr('class');
    });
    $('.del').on('click',function () {
        $(this).prev().remove('a');
        $(this).remove();
    });

};

//传url
var item,e_item;
function pass() {
    if (node_type=='Event'){
        var events=[];
        var event_1=[],event_2=[],event_3=[];
        var geo=$('#place').val();
        var time='';
        if (!$('.time').val()==''){
            time=Date.parse(new Date($('.time').val()))/1000;
        }
        var e_type=$('#event_type-1').val();
        var start='';
        if (!$('.start').val()==''){
            start=Date.parse(new Date($('.start').val()))/1000;
        };
        var end='';
        if (!$('.end').val()==''){
            end=Date.parse(new Date($('.end').val()))/1000;
        }
        //-----
        var rel_p=[];
        var person=$('#person').children('a');
        for (var p=0;p<person.length;p++){
            rel_p.push(person[p].text);
        };
        var user=rel_p.join(',');//参与人
        //-----
        var rel_o=[];
        var org=$('#org').children('a');
        for (var y=0;y<org.length;y++){
            rel_o.push(org[y].text);
        };
        var orgs=rel_o.join(',');//参与机构
        var desc=$('#e_business-1').val();
        //-----
        var tag=[];
        var e_tag=$('#e_tag').children('a');
        for (var p=0;p<e_tag.length;p++){
            tag.push(e_tag[p].text);
        };
        var tags=tag.join(',');
        //标签
        //------------
        var event_pass_url;
        event_pass_url='/construction/node_edit/?node_type='+node_type+'&item='+e_item+
            '&submit_user='+submit_user+'&real_geo='+geo+'&real_time='+time+
            '&event_type='+e_type+'&real_person='+user+'&real_auth='+orgs+'&start_ts='+start+
            '&end_ts='+end+'&description='+desc+'&work_tag='+tags+'&related_docs='+event_related_docs;
        console.log(event_pass_url)
        $.ajax({
            url: event_pass_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:yes_no
        });
    }else {
        var topic=[];
        $("#topic [name=rels]:checkbox:checked").each(function (index,item) {
            topic.push($(this).val());
        });
        var topic_string=topic.join(',')
        var domain=$('#ID-1').val();
        var function_description=$('#complie #business #business-1').val();
        var mark=[];
        $.each($('#tags').children('a'),function(index,item){
            mark.push($(item).text());
        })
        var function_mark=mark.join(',');
        var pass_url;
        if (function_description=='暂无'){
            pass_url='/construction/node_edit/?node_type='+node_type+'&item='+item+
                '&submit_user='+submit_user+'&topic_string='+topic_string+'&domain='+domain+
                '&function_mark='+function_mark+'&related_docs='+related_docs;
        }else {
            pass_url='/construction/node_edit/?node_type='+node_type+'&item='+item+
                '&submit_user='+submit_user+'&topic_string='+topic_string+'&domain='+domain+
                '&function_description='+function_description+'&function_mark='+function_mark+
                '&related_docs='+related_docs;
        }
        console.log(pass_url);
    }
    $('.group-1').css({display:'none'});
    $('.tags-1').css({display:'none'});
    $('.words-1').css({display:'none'});
    $('.group-1 input').val("");
    $('.tags-1 input').val("");
    $('.words-1 input').val("");
};
function yes_no(data) {
    console.log(data)
    if (data== true){
        alert('修改成功');
    }else {
        alert('修改失败');
    }
}

