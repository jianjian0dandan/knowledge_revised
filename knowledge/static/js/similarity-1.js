var types={
    'User':'人物',
    'Event':'事件',
    'Org':'机构',
    'Group':'群体',
    'SpecialEvent':'专题'
}
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
                title: "任务名称",//标题
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
                formatter: function (value, row, index) {
                    return types[row.node_type];
                }
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
                        return getLocalTime(row.submit_ts);
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
                    return '<a style="cursor: pointer;">查看</a>';
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            var name;
            if (value==''||value=='unknown'||value=='NULL'){
                name = row.node_id;
            }else {
                name = row.node_name;
            }
            if ($element[0].innerText=='查看') {
                if (row.compute_status==1){
                    window.open('/relation/similarity_result/?node_id='+row.node_id+'&node_type='+row.node_type+
                    '&name='+name);
                }else {
                    alert('未计算完成。');
                }

            }
        }
    });
};

function getLocalTime(nS) {
    var ns_len=nS.toString().length;
    if (ns_len>10){
        return new Date(parseInt(nS) ).toLocaleString();
    }else {
        return new Date(parseInt(nS) *1000 ).toLocaleString();
    }
};