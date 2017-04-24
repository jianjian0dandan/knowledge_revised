var key;
$('#container .new_property .pro_sure').on('click',function () {
    key=$('#container .new_property .key_words').val();
    var search_url='/group/search_related_people_item/?item='+key+'&submit_user='+submit_user;
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
                    if(row[1]==''||row[1]=='NULL'||row[1]=='unknown'){
                        return row[0];
                    }else {
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
                    if(row[2]==''||row[2]=='NULL'||row[2]=='unknown'){
                        return '暂无';
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
                    if(row[3]==''||row[3]=='NULL'||row[3]=='unknown'){
                        return 0;
                    }else {
                        return row[3].toFixed(2);
                    };
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
                    if(row[4]==''||row[4]=='NULL'||row[4]=='unknown'){
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
                    if(row[5]==''||row[5]=='NULL'||row[5]=='unknown'){
                        return 0;
                    }else {
                        return row[5].toFixed(2);
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
                    if (row[6].length==0||row[6]==''||row[6]=='NULL'||row[6]=='unknown'){
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
                title: '业务标签',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row[7].length==0||row[7]==''||row[7]=='NULL'||row[7]=='unknown'){
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
            groups.push(row[0]);
        },
        onUncheck:function (row) {
            groups.removeByValue(row[0]);
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
var groups=[];

$('.new_build').on('click',function () {
    var name=$('#container .new_property .theme_name').val();
    var tag=$('#container .new_property .theme_tag').val();
    if (name==''){
        alert('请输入您的群体名称。');
    }else {
        var node_ids=groups.join(',');
        add_url='/group/create_new_relation/?node1_id='+node_ids+'&node2_id='+name+
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
    console.log(data)
    if (data=='1'){
        alert('创建成功。');
    }else if(data=='group already exist') {
        alert('此群体已经存在，请检查您的群体名称。');
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