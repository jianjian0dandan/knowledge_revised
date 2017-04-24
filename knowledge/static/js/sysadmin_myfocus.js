
function call_sync_ajax_request(url, callback){
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      async: true,
      success:callback
    });
}

people_url='/sysadmin/focus/get_focus_people_data';
call_sync_ajax_request(people_url,draw_people_table);

people_url='/sysadmin/focus/get_focus_org_data';
call_sync_ajax_request(people_url,draw_org_table);

people_url='/sysadmin/focus/get_focus_event_data';
call_sync_ajax_request(people_url,draw_event_table);

//关注人物
function draw_people_table(data){
	console.log(data);
    data=eval(data);
    $('#person_table').bootstrapTable('load',data)
    $('#person_table').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40, 80],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: true,//回车搜索
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
            title: "人物名称",//标题
            field: "name",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            visible:true,
            formatter: function (value, row, index) {
                if (value==''||value=='null'||value=='unknown'){
                    return row.uid;
                }else {
                    return value;
                }
            },
        },
        {
            title: "ID",//标题
            field: "uid",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
        },
        {
            title: "业务标签",//标题
            field: "label",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value, row, index) {
                if (value)
                    return value;
                else
                    return '暂无';
            },
        },
        {
            title: "关注时间",//标题
            field: "time",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value, row, index) {
                if (value)
                    return value;
                else
                    return '暂无';
            },
        },
        {
            title: "群体查看",//标题
            field: "",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value,row) {
                var addr = '<a href="/index/person/?user_id='+row.uid+'" target="_blank"><span style="text-decoration:underline;font-weight:bold;">查看用户</span></a>'
                return addr;
            },
        },
        {
            title: "取消关注",//标题
            field: "",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value,row) {
                var n = '<span style="cursor:pointer;text-decoration:underline;font-weight:bold;color:#337ab7;"'+
                        ' onclick="dele_people(\''+ row.uid +'\')">取消关注</span> ';  
                return n;
            },
        }
        ]
    });
}

//关注机构
function draw_org_table(data){
	console.log(data);
    data=eval(data);
    $('#agencies_table').bootstrapTable('load',data)
    $('#agencies_table').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40, 80],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: true,//回车搜索
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
            title: "机构名称",//标题
            field: "name",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直 
            visible:true,
            formatter: function (value, row, index) {
                if (value==''||value=='null'||value=='unknown'){
                    return row.uid;
                }else {
                    return value;
                }
            },
        },
        {
            title: "ID",//标题
            field: "uid",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
        },
        {
            title: "业务标签",//标题
            field: "label",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value, row, index) {
                if (value)
                    return value;
                else
                    return '暂无';
            },
        },
        {
            title: "关注时间",//标题
            field: "time",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value, row, index) {
                if (value)
                    return value;
                else
                    return '暂无';
            },
        },
        {
            title: "机构查看",//标题
            field: "",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value,row) {
                var addr = '<a href="/index/organization/?user_id='+row.uid+'" target="_blank"><span style="text-decoration:underline;font-weight:bold;">查看机构</span></a>'
                return addr;
            },
        },
        {
            title: "取消关注",//标题
            field: "",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value,row) {
                var n = '<span style="cursor:pointer;text-decoration:underline;font-weight:bold;color:#337ab7;"'+
                        ' onclick="dele_org(\''+ row.uid +'\')">取消关注</span> ';  
                return n;
            },
        }
        ]
    });
}


//关注事件
function draw_event_table(data){
	console.log(data);
    data=eval(data);
    $('#events_table').bootstrapTable('load',data)
    $('#events_table').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40, 80],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: true,//回车搜索
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
            title: "事件名称",//标题
            field: "name",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            visible:true,
        },
        {
            title: "ID",//标题
            field: "uid",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            visible: false,
        },
        {
            title: "业务标签",//标题
            field: "label",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value, row, index) {
                if (value)
                    return value;
                else
                    return '暂无';
            },
        },
        {
            title: "关注时间",//标题
            field: "time",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value, row, index) {
                if (value)
                    return value;
                else
                    return '暂无';
            },
        },
        {
            title: "事件查看",//标题
            field: "",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value,row) {
                var addr = '<a href="/index/event/?user_id='+row.uid+'" target="_blank"><span style="text-decoration:underline;font-weight:bold;">查看事件</span></a>'
                return addr;
            },
        },
        {
            title: "取消关注",//标题
            field: "",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value,row) {
                var n = '<span style="cursor:pointer;text-decoration:underline;font-weight:bold;color:#337ab7;"'+
                        ' onclick="dele_event(\''+ row.uid +'\')">取消关注</span> ';  
                return n;
            },
        }
        ]
    });
}

function dele_people(data){
    var a = confirm('确定要取消关注该人物吗？');
    if (a == true){
        var url = '/sysadmin/delete_focus_people/?';
        url = url + 'people_id=' + data;
        console.log(url);
        call_sync_ajax_request(url,del);
        console.log('url');
    }
} 

function dele_org(data){
    var a = confirm('确定要取消关注该机构吗？');
    if (a == true){
        var url = '/sysadmin/delete_focus_org/?';
        url = url + 'org_id=' + data;
        console.log(url);
        call_sync_ajax_request(url,del);
        console.log('url');
    }
} 

function dele_event(data){
    var a = confirm('确定要取消关注该事件吗？');
    if (a == true){
        var url = '/sysadmin/delete_focus_event/?';
        url = url + 'event_id=' + data;
        console.log(url);
        call_sync_ajax_request(url,del);
        console.log('url');
    }
} 

function del(data){
    if(data=='success'){
        alert('操作成功！');
        location.reload();
    }
}