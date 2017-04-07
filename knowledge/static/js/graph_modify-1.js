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
                    return '<a>立即更新</a><a>编辑</a><a>删除</a>';
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
            console.log($element)
            console.log($element[0].childNodes.innerText)
            if ($element[0].childNodes[0]=='编辑') {
                console.log($element[0].childNodes.index())
            }
        }
    });
};

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
                    return '<a>立即更新</a> <a>编辑</a> <a>删除</a>';
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
        // onClickRow: function (row, tr) {
        //     if ($(tr.context).index()==2) {
        //         del_eventuid=row[0];
        //         $('#del_ject').modal("show");
        //     }
        // }
    });
};
