var key;
$('#container .new_property .pro_sure').on('click',function () {
    key=$('#container .new_property .key_words').val();
    var search_url='/theme/search_related_event_item/?item='+key+'&submit_user='+submit_user;
    $.ajax({
        url: search_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:search
    });
    $('.new_build').show();
});

function search(data) {
    var data=eval(data);
    console.log(data);
    $('#special_topic').bootstrapTable('load', data);
    $('#special_topic').bootstrapTable({
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
                    if(row[2]==''||row[2]=='NULL'||row[2]=='unknown'){
                        return '暂无';
                    }else {
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
                    if(row[3]==''||row[3]=='NULL'||row[3]=='unknown'){
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
                    if(row[4]==''||row[4]=='NULL'||row[4]=='unknown'){
                        return '暂无';
                    }else {
                        return row[4];
                    };
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
                    if(row[5]==''||row[5]=='NULL'||row[5]=='unknown'){
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
                    if(row[6]==''||row[6]=='NULL'||row[6]=='unknown'){
                        return '暂无';
                    }else {
                        return row[6];
                    }
                },
            },
            {
                title: '自动标签',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[7].length==0||row[7]==''||row[7]=='NULL'||row[7]=='unknown'){
                        return '暂无';
                    }else {
                        var tag='';
                        for (var k=0;k<row[7].length;k++){
                            tag+=row[7][k]+' ';
                        }
                        return tag;
                    }
                },
            },
            {
                title: '业务标签',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[8].length==0||row[8]==''||row[8]=='NULL'||row[8]=='unknown'){
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
            theme_list.push(row[0]);
        },
        onUncheck:function (row) {
            theme_list.removeByValue(row[0]);
        },
        // onClickCell: function (field, value, row, $element) {
        //     if ($element[0].innerText=='查看专题') {
        //         window.open('/theme/result/?theme_name='+row[1]);
        //     }else if ($element[0].innerText=='编辑专题') {
        //         // window.open(+row[1]);
        //     }
        // }
    });
}
var theme_list=[];

$('.new_build').on('click',function () {
    var name=$('#container .new_property .theme_name').val();
    var tag=$('#container .new_property .theme_tag').val();
    if (name==''){
        alert('请输入您的专题名称。');
    }else {
        var node_ids=theme_list.join(',');
        add_url='/theme/create_new_relation/?node1_id='+node_ids+'&node2_id='+name+
            '&submit_user='+submit_user+'&k_label='+tag;
        $.ajax({
            url: add_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:add
        });
    }
})
function add(data) {
    if (data=='success'){
        alert('创建成功。');
    }else if(data=='theme already exist') {
        alert('此专题已经存在，请检查您的专题名称。');
    }else {
        alert('创建失败。');
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