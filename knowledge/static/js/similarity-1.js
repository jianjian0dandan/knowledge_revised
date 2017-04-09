//计算任务
var calculation_url='/relation/all_sim/';
$.ajax({
    url: calculation_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:calculation
});
function calculation(data) {
    var data = eval(data);
    console.log(data)
    $('#task').bootstrapTable('load', data);
    $('#task').bootstrapTable({
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
                title: "节点名称",//标题
                field: "node_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return row.node_id;
                    }else {
                        return row.node_name;
                    }
                }
            },
            {
                title: "节点类型",//标题
                field: "node_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //
                // }
            },
            {
                title: "提交时间",//标题
                field: "submit_ts",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {

                        var to_time=getLocalTime(row.submit_ts.toString());
                        var pattern = /[\u4e00-\u9fa5]/;
                        var time=to_time.replace(/pattern/,'');
                        return time;
                    }
                },
            },
            // {
            //     title: "相似节点ID",//标题
            //     field: "related_id",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (value==''||value=='unknown'||value=='NULL'){
            //             return '暂无';
            //         }else {
            //             var words=row.related_id.split('&');
            //             if (words.length<=5){
            //                 return words.join(',');
            //             }else {
            //                 var key=words.splice(0,5).join(',');
            //                 var tit=words.splice(5).join(',');
            //                 return '<p title="'+tit+'">'+key+'</p> ';
            //             }
            //         }
            //     },
            // },
            {
                title: "计算进度",//标题
                field: "compute_status",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==0){
                        return '未计算';
                    }else if (value== -1){
                        return '正在计算';
                    }else if (value==1){
                        return '计算完成';
                    }
                },
            },
            {
                title: "查看",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a>查看</a>';
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='查看') {
                if (row.compute_status==1){
                    window.open('/relation/similarity_result/?node_id='+row.node_id+'&node_type='+row.node_type);
                }else {
                    alert('未计算完成。');
                }

            }
        }
    });
};


function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString();
};