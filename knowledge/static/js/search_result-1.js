var lation={
    "friend" :"交互",
    "relative" :"亲属",
    "leader" :"上下级关系",
    "colleague" :"自述关联",
    "ip_relation" :"IP关联",
    "user_tag":"其他关系",
    "friend" :"交互",
    "colleague" :"业务关联",
    "organization_tag":"其他",
    "contain"  :"主题关联",
    'event_other':"其他关系",
    "join" :" 参与事件",
    "discuss":"参与舆论",
    "other_relationship" :"其他关系",
    "wiki_link":"维基百科"
};
var _event_type={
    'military':'军事国防',
    'transport':'交通',
    'resources':'国土资源',
    'overseas':'境外敌对势力',
    'disaster':'灾害',
    'public_security':'社会公共安全',
    'rights':'维权上访',
    'information':'信息产业',
    'information_security':'信息安全',
    'industry':'工业',
    'network':'网络安全',
    'chinese_party':'中国共产党党务',
    'national':'国家政务',
    'diplomacy':'外交',
    'political':'政法监察',
    'comprehensive_group':'综合党团',
    'health':'卫生',
    'art_sports':'文化体育',
    'tourism':'旅游服务',
    'human_resources':'人力资源与社会保障',
    'population':'人口计生',
    'agriculture':'农业',
    'housing':'住房与城乡建设',
    'environment':'环境保护',
    'energy':'能源',
    'technology':'科技教育',
    'business':'商业贸易',
    'macro_economy':'宏观经济',
    'financial_work':'财政金融',
    'other':'其他'
}

var result_url;
if (simple_advanced=='s'){
    result_url='/relation/simple_result/?submit_user='+submit_user+'&keywords='+key_words;
}else {
    advanced_search_url='/relation/submit_task/';
    $.ajax({
        type:'POST',
        url: advanced_search_url,
        contentType:"application/json",
        data: JSON.stringify(input_data),
        dataType: "json",
        success: result
    });
}
$.ajax({
    url: result_url,
    type: 'GET',
    dataType: 'json',
    async: true,
    success:result
});
var graph_force=[];
var graph_picture;
function result(data) {
    console.log(data)
    if (simple_advanced=='s'){
        var data=eval(data);
        $('.related_network').hide();
        graph_picture = data.graph_result;
        person(data.table_result.p_nodes);
        agencies(data.table_result.o_nodes);
        _events(data.table_result.e_nodes);
        organization(data.table_result.g_nodes);
        subject(data.table_result.s_nodes);
    }else {
        $('.related_network').show();
        if(data=='no start id'){
            alert('搜不到对应条件的起始节点');
        }else if(data=='short_path no end id') {
            alert('搜不到对应条件的终止节点');
        }else {
            var data=eval(data);
            // network(data.graph_result);
            graph_picture = data.graph_result;
            person(data.table_result.p_nodes);
            agencies(data.table_result.o_nodes);
            _events(data.table_result.e_nodes);
            organization(data.table_result.g_nodes);
            subject(data.table_result.s_nodes);
        }
    }
}

//相关网络
// function network(n_data) {
//     $('.network_1').css({display:'none'});
//     var n_data = eval(n_data);
//     var links = [];
//     $.each(n_data,function (index,item) {
//         var type1;
//         for (var key in item[0]){
//             type1=key;
//             break;
//         }
//         var type2;
//         for (var key in item[2]){
//             type2=key;
//             break;
//         }
//         var source,target;
//         if (item[0].name==''||item[0].name=='unknown'){
//             source=item[0].event_id||item[0].org_id||item[0].uid;
//         }else {
//             source=item[0].name;
//         }
//         if (item[2].name==''||item[2].name=='unknown'){
//             target=item[2].uid||item[2].event_id||item[2].org_id;
//         }else {
//             target=item[2].name;
//         }
//         links.push({source:source,type1:item[0],type2:type2, target:target,rel:lation[item[1]]});
//     });
//     var nodes = {};
//
//     links.forEach(function(link) {
//         link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
//         link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
//     });
//
//     var width = 950,
//         height = 500;
//
//     var force = d3.layout.force()//layout将json格式转化为力学图可用的格式
//         .nodes(d3.values(nodes))//设定节点数组
//         .links(links)//设定连线数组
//         .size([width, height])//作用域的大小
//         .linkDistance(200)//连接线长度
//         .charge(-50)//顶点的电荷数。该参数决定是排斥还是吸引，数值越小越互相排斥
//         .on("tick", tick)//指时间间隔，隔一段时间刷新一次画面
//         .start();//开始转换
//
//     var svg = d3.select("#network").append("svg")
//         .attr("width", width)
//         .attr("height", height);
//
//     //箭头
//     var marker=
//         svg.append("marker")
//         //.attr("id", function(d) { return d; })
//             .attr("id", "resolved")
//             //.attr("markerUnits","strokeWidth")//设置为strokeWidth箭头会随着线的粗细发生变化
//             .attr("markerUnits","userSpaceOnUse")
//             .attr("viewBox", "0 -5 10 10")//坐标系的区域
//             .attr("refX",32)//箭头坐标
//             .attr("refY", -1)
//             .attr("markerWidth", 12)//标识的大小
//             .attr("markerHeight", 12)
//             .attr("orient", "auto")//绘制方向，可设定为：auto（自动确认方向）和 角度值
//             .attr("stroke-width",2)//箭头宽度
//             .append("path")
//             .attr("d", "M0,-5L10,0L0,5")//箭头的路径
//             .attr('fill','#000000');//箭头颜色
//
//     //    将连接线设置为曲线
//
//     //设置连接线
//     var edges_line = svg.selectAll(".edgepath")
//         .data(force.links())
//         .enter()
//         .append("path")
//         .attr({
//             'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
//             'class':'edgepath',
//             //'fill-opacity':0,
//             //'stroke-opacity':0,
//             //'fill':'blue',
//             //'stroke':'red',
//             'id':function(d,i) {return 'edgepath'+i;}})
//         .style("stroke",function(d){
//             var lineColor;
//             //根据关系的不同设置线条颜色
//             if(d.type2=="enent_id"){
//                 lineColor="#d9b3e6";
//             }else if(d.type2=="uid"){
//                 lineColor="#81c2d6";
//             }else if(d.type2=="uid"){
//                 lineColor="#e62144";
//             }
//             return lineColor;
//         })
//         .style("pointer-events", "none")
//         .style("stroke-width",1.5)//线条粗细
//         .attr("marker-end", "url(#resolved)" );//根据箭头标记的id号标记箭头
//
//     var edges_text = svg.append("g").selectAll(".edgelabel")
//         .data(force.links())
//         .enter()
//         .append("text")
//         .style("pointer-events", "none")
//         //.attr("class","linetext")
//         .attr({
//             'class':'edgelabel',
//             'id':function(d,i){return 'edgepath'+i;},
//             'dx':80,
//             'dy':0
//             //'font-size':10,
//             //'fill':'#aaa'
//         });
//
//     //设置线条上的文字
//     edges_text.append('textPath')
//         .attr('xlink:href',function(d,i) {return '#edgepath'+i})
//         .style("pointer-events", "none")
//         .text(function(d){return d.type1;});
//
//     //圆圈
//     var circle = svg.append("g").selectAll("circle")
//         .data(force.nodes())//表示使用force.nodes数据
//         .enter().append("circle")
//         .style("fill",function(node){
//             var color;//圆圈背景色
//             // var link=links[node.index];
//             if(node.type2=="enent_id"){
//                 color="#F6E8E9";
//             }else if(node.type2=="uid"){
//                 color="rgb(243, 25, 47)";
//             }else{
//                 color="#00d464";
//             }
//             return color;
//         })
//         .style('stroke',function(node){
//             var color;//圆圈线条的颜色
//             // var link=links[node.index];
//             if(node.type2=="enent_id"){
//                 color="#673ab7";
//             }else if(node.type2=="uid"){
//                 color="#03A9F4";
//             }else{
//                 color="#e91e63";
//             }
//             return color;
//         })
//         .attr("r", 28)//设置圆圈半径
//         .on("click",function(node){
//             //单击时让连接线加粗
//             edges_line.style("stroke-width",function(line){
//                 if(line.source.name==node.name || line.target.name==node.name){
//                     return 4;
//                 }else{
//                     return 1.5;
//                 }
//             });
//             //d3.select(this).style('stroke-width',2);
//         })
//         //双击跳转
//         .on("dblclick",function(node){
//             console.log(node)
//         })
//         .call(force.drag);//将当前选中的元素传到drag函数中，使顶点可以被拖动
//
//     var text = svg.append("g").selectAll("text")
//         .data(force.nodes())
//         //返回缺失元素的占位对象（placeholder），指向绑定的数据中比选定元素集多出的一部分元素。
//         .enter()
//         .append("text")
//         .attr("dy", ".35em")
//         .attr("text-anchor", "middle")//在圆圈中加上数据
//         .style('fill',function(node){
//             var color;//文字颜色
//             // var link=links[node.index];
//             if(node.type2=="enent_id"){
//                 color="#F6E8E9";
//             }else if(node.type2=="uid"){
//                 color="rgb(243, 25, 47)";
//             }else{
//                 color="#00d464";
//             }
//             return color;
//         }).attr('x',function(d){
//             // console.log(d.name+"---"+ d.name.length);
//             var re_en = /[a-zA-Z]+/g;
//             //如果是全英文，不换行
//             if(d.name.match(re_en)){
//                 d3.select(this).append('tspan')
//                     .attr('x',0)
//                     .attr('y',2)
//                     .text(function(){return d.name;});
//             }
//             //如果小于四个字符，不换行
//             else if(d.name.length<=4){
//                 d3.select(this).append('tspan')
//                     .attr('x',0)
//                     .attr('y',2)
//                     .text(function(){return d.name;});
//             }else{
//                 var top=d.name.substring(0,4);
//                 var bot=d.name.substring(4,d.name.length);
//
//                 d3.select(this).text(function(){return '';});
//
//                 d3.select(this).append('tspan')
//                     .attr('x',0)
//                     .attr('y',-7)
//                     .text(function(){return top;});
//
//                 d3.select(this).append('tspan')
//                     .attr('x',0)
//                     .attr('y',10)
//                     .text(function(){return bot;});
//             }
//             //直接显示文字
//             /*.text(function(d) {
//              return d.name; */
//         });
//
//
//     function tick() {
//         //path.attr("d", linkArc);//连接线
//         circle.attr("transform", transform1);//圆圈
//         text.attr("transform", transform2);//顶点文字
//
//
//         edges_line.attr('d', function(d) {
//             var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
//             return path;
//         });
//
//         edges_text.attr('transform',function(d,i){
//             if (d.target.x<d.source.x){
//                 bbox = this.getBBox();
//                 rx = bbox.x+bbox.width/2;
//                 ry = bbox.y+bbox.height/2;
//                 return 'rotate(180 '+rx+' '+ry+')';
//             }
//             else {
//                 return 'rotate(0)';
//             }
//         });
//     }
//
//     //设置连接线的坐标,使用椭圆弧路径段双向编码
//     function linkArc(d) {
//          return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y
//     }
//     //设置圆圈和文字的坐标
//     function transform1(d) {
//         return "translate(" + d.x + "," + d.y + ")";
//     }
//     function transform2(d) {
//         return "translate(" + (d.x) + "," + d.y + ")";
//     }
//
// }




//相关人物
var people;
function person(p_data) {
    var p_data = eval(p_data);
    people=p_data;
    $('.person_1').css({display:'none'});
    $('#person').bootstrapTable('load', p_data);
    $('#person').bootstrapTable({
        data:p_data,
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
                field: "uid",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "人物昵称",//标题
                field: "uname",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return row.uid;
                    }else {
                        return row.uname;
                    }
                }
            },
            {
                title: "注册地",//标题
                field: "location",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '未知';
                    }else {
                        return row.location;
                    }
                },
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.influence.toFixed(2);
                    }
                },
            },
            {
                title: "活跃度",//标题
                field: "activeness",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.activeness.toFixed(2);
                    }
                },
            },
            {
                title: "敏感度",//标题
                field: "sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.sensitive.toFixed(2);
                    }
                },
            },
            {
                title: "自动标签",//标题
                field: "keywords_string",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=row.keywords_string.split('&');
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
                title: "计算状态",//标题
                field: "sim",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value=='not exist'){
                        var infor=row.uname+','+row.uid+',User';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var name;
                        if (row.uname==''||row.uname=='unknown'||row.uname=='NULL'){
                            name = row.uid;
                        }else {
                            name = row.uname;
                        }
                        var go=row.uid+',User,'+name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if (field=='uid'){
                window.open('/index/person/?user_id='+value)
            }
        }
    });
};

//相关机构
var org;
function agencies(data) {
    var data = eval(data);
    org=data;
    $('.agencies_1').css({display:'none'});
    $('#agencies').bootstrapTable('load', data);
    $('#agencies').bootstrapTable({
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
                title: "ID",//标题
                field: "id",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "机构名称",//标题
                field: "uname",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return row.uid;
                    }else {
                        return row.uname;
                    }
                }
            },
            {
                title: "注册地",//标题
                field: "location",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '未知';
                    }else {
                        return row.location;
                    }
                },
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.influence.toFixed(2);
                    }
                },
            },
            {
                title: "活跃度",//标题
                field: "activeness",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.activeness.toFixed(2);
                    }
                },
            },
            {
                title: "敏感度",//标题
                field: "sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.sensitive.toFixed(2);
                    }
                },
            },
            {
                title: "自动标签",//标题
                field: "keywords_string",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=row.keywords_string.split('&');
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
                title: "计算状态",//标题
                field: "sim",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value=='not exist'){
                        var infor=row.uname+','+row.id+',Org';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var name;
                        if (row.uname==''||row.uname=='unknown'||row.uname=='NULL'){
                            name = row.uid;
                        }else {
                            name = row.uname;
                        }
                        var go=row.id+',Org,'+name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if (field=='id'){
                window.open('/index/organization/?user_id='+value)
            }
        }
    });
};

//相关事件
var events;
function _events(e_data) {
    console.log(11)
    var e_data = eval(e_data);
    events=e_data;
    $('.events_1').css({display:'none'});
    $('#events').bootstrapTable('load', e_data);
    $('#events').bootstrapTable({
        data:e_data,
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
                title: "事件名称",//标题
                field: "name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "事件类型",//标题
                field: "event_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else{
                        return _event_type[value];
                    }
                }
            },
            {
                title: "发生时间",//标题
                field: "real_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else if (!isNaN(value)){
                        return getLocalTime(value);
                    }else {
                        return row.real_time;
                    }
                },
            },
            {
                title: "发生地点",//标题
                field: "real_geo",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        return row.real_geo;
                    }
                },
            },
            {
                title: "参与人数",//标题
                field: "uid_counts",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.uid_counts;
                    }
                },
            },
            {
                title: "微博数量",//标题
                field: "weibo_counts",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.weibo_counts;
                    }
                },
            },
            {
                title: "自动标签",//标题
                field: "keywords",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=row.keywords.split('&');
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
                title: "计算状态",//标题
                field: "sim",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value=='not exist'){
                        var infor=row.name+','+row.id+',Event';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var go=row.id+',Event,'+row.name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if (field=='name'){
                window.open('/index/event/?user_id='+row.id);
            }
        }
    });
};

//相关群体
var group;
function organization(data) {
    var data = eval(data);
    group=data;
    $('.organization_1').css({display:'none'});
    $('#organization').bootstrapTable('load', data);
    $('#organization').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20, 40],//分页步进值
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
                title: "群体名称",//标题
                field: "group_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return row.id;
                    }else {
                        return row.group_name;
                    }
                }
            },
            {
                title: "自动标签",//标题
                field: "label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=value.split('&');
                        if (words.length<=5){
                            return words.join(',');
                        }else {
                            var key=words.splice(0,5).join(',');
                            var tit=words.splice(5).join(',');
                            return '<p title="'+tit+'">'+key+'</p> ';
                        };
                    }
                }
            },
            {
                title: "业务标签",//标题
                field: "k_label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                		var words=value;
                    if (words.length==0){
                        return '暂无';
                    }else {
                        //var words=value.split('&');
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
                title: "参与人数",//标题
                field: "people_count",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.people_count;
                    }
                },
            },
            {
                title: "创建时间",//标题
                field: "create_ts",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        return getLocalTime(row.create_ts);
                    }
                },
            },
            {
                title: "计算状态",//标题
                field: "sim",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value=='not exist'){
                        var infor=row.group_name+','+row.id+',Group';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var name;
                        if (row.group_name==''||row.group_name=='unknown'||row.group_name=='NULL'){
                            name= row.id;
                        }else {
                            name= row.group_name;
                        }
                        var go=row.id+',Group,'+name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if (field=='group_name'){
                window.open('/group/result/?group_name='+row.group_name);
            }
        }
    });
};

//相关专题
var theme;
function subject(data) {
    var data = eval(data);
    theme=data;
    $('.subject_1').css({display:'none'});
    $('#subject').bootstrapTable('load', data);
    $('#subject').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [5, 20],//分页步进值
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
                title: "专题名称",//标题
                field: "topic_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return row.id;
                    }else {
                        return row.topic_name;
                    }
                }
            },
            {
                title: "自动标签",//标题
                field: "label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=value.split('&');
                        if (words.length<=5){
                            return words.join(',');
                        }else {
                            var key=words.splice(0,5).join(',');
                            var tit=words.splice(5).join(',');
                            return '<p title="'+tit+'">'+key+'</p> ';
                        }
                    }
                }
            },
            {
                title: "业务标签",//标题
                field: "k_label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                		var words=value;
                    if (words.length==0){
                        return '暂无';
                    }else {
                        //var words=value.split('&');
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
                title: "包含事件数量",//标题
                field: "event_count",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return 0;
                    }else {
                        return row.event_count;
                    }
                },
            },
            {
                title: "创建时间",//标题
                field: "create_ts",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        return getLocalTime(row.create_ts);
                    }
                },
            },
            {
                title: "计算状态",//标题
                field: "sim",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value=='not exist'){
                        var infor=row.topic_name+','+row.id+',SpecialEvent';
                        return '无相似计算任务'+'<br/><a style="cursor: pointer;" onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                    		var name;
                        if (row.topic_name==''||row.topic_name=='unknown'||row.topic_name=='NULL'){
                            name= row.id;
                        }else {
                            name= row.topic_name;
                        }
                        var go=row.id+',SpecialEvent,'+name;
                        return '<a style="cursor: pointer;" onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if (field=='topic_name'){
                window.open('/theme/result/?theme_name='+row.topic_name);
            }
        }
    });
};

function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().substr(0,10);
};
function add_new_task(row) {
    var information=row.split(',');
    var time=Date.parse(new Date());
    var creat_url='/relation/compute_sim/?submit_user='+submit_user+'&submit_ts='+time+
        '&node_name='+information[0]+'&node_id='+information[1]+'&node_type='+information[2];
    $.ajax({
        url: creat_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:function (data) {
            if (data=='yes'){
                alert('创建成功。');
                $.ajax({
                    url: result_url,
                    type: 'GET',
                    dataType: 'json',
                    async: true,
                    success:result
                });
            }else {
                alert('创建失败。');
            }
        }
    });
}

function go_jump(uid_type) {
    var news=uid_type.split(',');
    window.open('/relation/similarity_result/?node_id='+news[0]+'&node_type='+news[1]+'&name='+news[2]);
};

var result_obj,event_obj=[],org_obj=[],people_obj=[];
result_obj={'event':event_obj,'org':org_obj,'people':people_obj};
$('#map').on('click',function () {
    $.each(people,function (index,item) {
        var p_arr=[];
        p_arr.push(item.uid);
        p_arr.push(item.uname);
        p_arr.push(item.location);
        people_obj.push(p_arr);
    });
    $.each(org,function (index,item) {
        var o_arr=[];
        o_arr.push(item.id);
        o_arr.push(item.uname);
        o_arr.push(item.location);
        org_obj.push(o_arr);
    })
    $.each(events,function (index,item) {
        var e_arr=[];
        e_arr.push(item.id);
        e_arr.push(item.name);
        e_arr.push(item.real_geo);
        event_obj.push(e_arr);
    });
    result_obj=JSON.stringify(result_obj);
    localStorage.setItem('result_map',result_obj);
    window.open('/index/map/');
});

$('#chart').on('click',function () {
    $.each(graph_picture,function (index,item) {
        var gra=[];
        var gra_1={};
        for (var key in item[0]){
            if( !(key == 'name') ){
                gra_1['id']=item[0][key];
                if (key=='event_id'){
                    gra_1['lx']='event';
                }else if (key=='uid'){
                    gra_1['lx']='people';
                }else if (key=='org_id'){
                    gra_1['lx']='org';
                }else if (key=='event'){
                    gra_1['lx']='topic';
                }else if (key=='group'){
                    gra_1['lx']='group';
                }else if (key=='url'){
                    gra_1['lx']='wiki';
                }
            }else {
                gra_1['head']=item[0][key];
            }
        };
        var gra_2={};
        for (var key2 in item[2]){
            if( !(key2 == 'name') ){
                gra_2['id']=item[2][key2];
                if (key2=='event_id'){
                    gra_2['lx']='event';
                }else if (key2=='uid'){
                    gra_2['lx']='people';
                }else if (key2=='org_id'){
                    gra_2['lx']='org';
                }else if (key2=='event'){
                    gra_2['lx']='topic';
                }else if (key2=='group'){
                    gra_2['lx']='group';
                }else if (key2=='url'){
                    gra_2['lx']='wiki';
                }
            }else {
                gra_2['head']=item[2][key2];
            }
        };
        gra.push(gra_1['id']);gra.push(gra_1['head']);gra.push(gra_1['lx']);
        gra.push(gra_2['id']);gra.push(gra_2['head']);gra.push(gra_2['lx']);
        gra.push(item[1]);
        graph_force.push(gra);
    });
    graph_force=JSON.stringify(graph_force);
    localStorage.setItem('graph_force',graph_force);
    window.open('/index/graph_index/?flag_type=nana');
});

setTimeout(function () {
    localStorage.removeItem('temp');
},600000);

