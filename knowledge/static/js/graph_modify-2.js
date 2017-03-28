//关系选择
var start_type='User',end_type='User';
function one_type(value) {
    start_type=value;
};
function two_type(value) {
    end_type=value;
};

//类似百度搜索功能
var one_value='',two_value='',search_data_url;
$('.manone').bind('input propertychange', function() {
    one_value=$('.manone').val();
    search_data_url='/construction/search_node/?node_type='+start_type+'&item='+one_value;
    $.ajax({
        url: search_data_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:search_data
    });
});
$('.mantwo').bind('input propertychange', function() {
    two_value=$('.mantwo').val();
    search_data_url='/construction/search_node/?node_type='+end_type+'&item='+two_value;
    $.ajax({
        url: search_data_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:search_data
    });

});

var data = [];
function search_data(look) {
    var data_result=eval(look);
    if (start_type=='Event'||end_type=='Event'){
        $.each(data_result,function (index,item) {
            data.push(item[1]+'<span class="_id" style="display:none;">'+item[0]+'</span>');
            if (start_type=='Event'){
                uid_1_name=item[1];
            }else {
                uid_2_name=item[1];
            }
        })
    }else {
        $.each(data_result,function (index,item) {
            if (item[1]==''||item[1]=='unknown'){
                data.push(item[0]+'<span class="_id" style="display:none;">'+item[0]+'</span>');
            }else {
                data.push(item[1]+'('+item[0]+')'+'<span class="_id" style="display:none;">'+item[0]+'</span>');
            }

        })
    }
}

var in_class;
function class_name(input_class) {
    in_class=$(input_class).attr('class');
}
var uid_1,uid_2,uid_1_name,uid_2_name;

$(document).ready(function(){
    $('.manone').attr('disabled',false);
    $(document).keydown(function(e){
        e = e || window.event;
        var keycode = e.which ? e.which : e.keyCode;
        if(keycode == 38){
            if (in_class=='manone'){
                if(jQuery.trim($('.append-1').html())==''){
                    return;
                }
            }else {
                if(jQuery.trim($('.append-2').html())==''){
                    return;
                }
            }
            movePrev();
        }else if(keycode == 40){
            if (in_class=='manone'){
                if(jQuery.trim($('.append-1').html())==''){
                    return;
                }
                $('#container .rel_attributes .one .manone').blur();
            }else {
                if(jQuery.trim($('.append-2').html())==''){
                    return;
                }
                $('#container .rel_attributes .two .mantwo').blur();
            }
            if($('.item').hasClass('addbg')){
                moveNext();
            }else{
                $('.item').removeClass('addbg').eq(0).addClass('addbg');
            }
        }else if(keycode == 13){
            dojob();
        }
    });
    var movePrev = function(){
        if (in_class=='manone'){
            $('#container .rel_attributes .one .manone').blur();
        }else {
            $('#container .rel_attributes .two .mantwo').blur();
        }
        var index = $('.addbg').prevAll().length;
        if(index == 0){
            $('.item').removeClass('addbg').eq($('.item').length-1).addClass('addbg');
        }else{
            $('.item').removeClass('addbg').eq(index-1).addClass('addbg');
        }
    }
    var moveNext = function(){
        var index = $('.addbg').prevAll().length;
        if(index == $('.item').length-1){
            $('.item').removeClass('addbg').eq(0).addClass('addbg');
        }else{
            $('.item').removeClass('addbg').eq(index+1).addClass('addbg');
        }
    };
    var dojob = function(){
        if (in_class=='manone'){
            $('#container .rel_attributes .one .manone').blur();
            var value = $('.addbg').text();
            uid_1=$('.addbg').children('._id').text();
            $('#container .rel_attributes .one .manone').val(value);
            $('.append-1').hide().html('');
            $('.manone').attr('disabled',true);
        }else {
            $('#container .rel_attributes .two .mantwo').blur();
            var value = $('.addbg').text();
            uid_2=$('.addbg').children('._id').text();
            $('#container .rel_attributes .two .mantwo').val(value);
            $('.append-2').hide().html('');
            $('.mantwo').attr('disabled',true);
        }

    }
});
function getContent(obj){
    var kw = jQuery.trim($(obj).val());
    if(kw == ''){
        if (in_class=='manone'){
            $('.append-1').hide().html('');
        }else {
            $('.append-2').hide().html('');
        }
        return false;
    }
    var html = '';
    for (var i = 0; i < data.length; i++) {
        if (data[i].indexOf(kw) >= 0) {
            html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon(this);'>" + data[i] + "</div>"
        }
    }
    if(html != ''){
        if (in_class=='manone'){
            $('.append-1').show().html(html);
        }else {
            $('.append-2').show().html(html);
        }
    }else{
        if (in_class=='manone'){
            $('.append-1').hide().html('');
        }else {
            $('.append-2').hide().html('');
        }
    }
    data = [];
}
function getFocus(obj){
    $('.item').removeClass('addbg');
    $(obj).addClass('addbg');
}
function getCon(obj){
    var value = $(obj).text();
    if (in_class=='manone'){
        $('#container .rel_attributes .one .manone').val(value);
        $('.append-1').hide().html('');
        uid_1=$(obj).find('._id').text();
        console.log($(obj))
        uid_1_name=$(obj).find('._id').text();
        $('.manone').attr('disabled',true);
    }else {
        $('#container .rel_attributes .two .mantwo').val(value);
        $('.append-2').hide().html('');
        uid_2=$(obj).find('._id').text();
        $('.mantwo').attr('disabled',true);
    }

}

//---类似百度搜索功能----完---

$('#container .rel_submit').on('click',function () {
    console.log(uid_1_name,uid_2_name)
    var name_type_1,name_type_2,name_index_1,name_index_2;
    var input_data=[];
    if (start_type=='User'||end_type=='User'){
        name_type_1='uid';
        name_index_1='node_index';
        name_type_2='uid';
        name_index_2='node_index';
    }else if(start_type=='Org'||end_type=='Org') {
        name_type_1='org_id';
        name_index_1='org_index';
        name_type_2='org_id';
        name_index_2='org_index';
    }else if(start_type=='Event'||end_type=='Event') {
        name_type_1='event_id';
        name_index_1='event_index';
        name_type_2='event_id';
        name_index_2='event_index';
    }
    input_data.push([
        name_type_1, uid_1, name_index_1,
        name_type_2, uid_2, name_index_2
    ]);
    var input_url='/construction/relation_show_edit/';
    $.ajax({
        type:'POST',
        url: input_url,
        contentType:"application/json",
        data: JSON.stringify(input_data),
        dataType: "json",
        success: relation_add
    });
    console.log(input_data)
})
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
function relation_add(data) {
    var data=eval(data);
    console.log(data)
    rel_list(data);
}
function rel_list(data) {
    var data = eval(data);
    $('#rel_list').bootstrapTable('load', data);
    $('#rel_list').bootstrapTable({
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
                title: "节点1",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return uid_1_name;
                }
            },
            {
                title: "节点2",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return uid_2_name;
                },
            },
            {
                title: "关系",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row;
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
                    return '编辑';
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

        ],
        // onClickRow: function (row, tr) {
        //     if ($(tr.context).index()==2) {
        //         del_eventuid=row[0];
        //         $('#del_ject').modal("show");
        //     }
        // }
    });
};