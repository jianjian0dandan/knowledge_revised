function fans() {
    this.ajax_method = 'GET';
}
fans.prototype= {
    call_request:function(url,callback) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:callback,
        });
    },
}
function friendfans(data) {
     //console.log("outdata="+data);
     $('#table-user').bootstrapTable({
       //url: influ_url,
       data:data,
       search: false,//是否搜索
       pagination: true,//是否分页
       pageSize: 20,//单页记录数
       pageList: [5, 10, 20, 50],//分页步进值
       sidePagination: "client",//服务端分页
       searchAlign: "left",
       searchOnEnterKey: false,//回车搜索
       showRefresh: true,//刷新按钮
       showColumns: true,//列选择按钮
       buttonsAlign: "left",//按钮对齐方式
       locale: "zh-CN",//中文支持
       detailView: false,
       showToggle:true,
       sortName:'count',
       sortOrder:"desc",
       columns: [  
         {
             title: "全选",
             field: "select",
             checkbox: true,
             align: "center",//水平
             valign: "middle"//垂直
         },
         {
             title: "头像",
             field: "photo_url",
             sortable: true,
             align: "center",//水平
             valign: "middle",//垂直
             formatter: function (value) {
               var photo_url = value;
               if(value=="unknown"||value==""||value==null){
                 photo_url = "http://tva1.sinaimg.cn/default/images/default_avatar_male_50.gif";
               }
               return '<img  src="'+photo_url+'" class="img-rounded" style="width: 30px;height: 30px;}" >';
             }
         },
         {
             title: "昵称",
             field: "uname",
             align: "center",//水平
             valign: "middle",//垂直
             formatter: function (value,row) { 
               if(value=="unknown"||value==""||value==null){
                 value = "未知";
                 return value
               }else{
               var e = '<a class="user_view" data-toggle="tooltip" title="看看TA是谁？" data-placement="right" href="/index/viewinformation/?uid='+row.uid+' "target="_blank">'+value+'</a>';   ///index/viewinformation/?uid=\''+row.uid+'\'
                return e;
              }
            }
         },
         {
             title: "用户ID",
             field: "uid",
             align: "center",//水平
             valign: "middle",//垂直
             visible:false
         },
         {
             title: "好友数",                        
             field: "friendsnum",
             sortable: true,
             align: "center",//水平
             valign: "middle",//垂直
             formatter: function (value) {
                if(value=="unknown"||value==""||value==null){
                 value = "未知";
               }
                return value;
             }
         },
         {
             title: "粉丝数",                        
             field: "fansnum",
             sortable: true,
             align: "center",//水平
             valign: "middle",//垂直
             formatter: function (value) {
                if(value=="unknown"||value==""||value==null){
                 value = "未知";
               }
                return value;
             }
         },
         {
             title: "微博数",                        
             field: "weibo_count",
             sortable: true,
             align: "center",//水平
             valign: "middle",//垂直
             formatter: function (value) {
                if(value=="unknown"||value==""||value==null){
                 value = "未知";
               }
                return value;
             }
         },
         {
             title: "交互次数",                        
             field: "count",
             sortable: true,
             align: "center",//水平
             valign: "middle",//垂直
             formatter: function (value) {
                if(value=="unknown"||value==""||value==null){
                 value = "未知";
               }
                return value;
             }

        }]
     });
}

var fans=new fans();
function nums() {
    var url = '/info_person_social/get_fans/?uid='+uid;
    fans.call_request(url,friendfans);
}

$('#fan_btn').click(function(){
    nums();
    console.log("点击加载");
});

