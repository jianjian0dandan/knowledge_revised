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
function result(data) {
    console.log(data)
    var data=eval(data);
    if (simple_advanced=='s'){
        $('.related_network').hide();
        person(data.p_nodes);
        agencies(data.o_nodes);
        events(data.e_nodes);
        organization(data.g_nodes);
        subject(data.s_nodes);
    }else {
        $('.related_network').show();
        network(data.graph_result);
        person(data.table_result.p_nodes);
        agencies(data.table_result.o_nodes);
        events(data.table_result.e_nodes);
        organization(data.table_result.g_nodes);
        subject(data.table_result.s_nodes);
    }

}
//相关网络
function network(n_data) {
    var n_data = eval(n_data);
    var links = [];
    $.each(n_data,function (index,item) {
        var type2;
        for (var key in item[0]){
            type2=key;
            break;
        }
        var source,target;
        if (item[0].name==''||item[0].name=='unknown'){
            source=item[0].event_id||item[0].org_id||item[0].uid;
        }else {
            source=item[0].name;
        }
        if (item[2].name==''||item[2].name=='unknown'){
            target=item[2].uid||item[2].event_id||item[2].org_id;
        }else {
            target=item[2].name;
        }
        links.push({source:source,type1:item[1],type2:type2, target:target,});
    });
    var nodes = {};

    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
    });

    var width = 950,
        height = 500;

    var force = d3.layout.force()//layout将json格式转化为力学图可用的格式
        .nodes(d3.values(nodes))//设定节点数组
        .links(links)//设定连线数组
        .size([width, height])//作用域的大小
        .linkDistance(200)//连接线长度
        .charge(-50)//顶点的电荷数。该参数决定是排斥还是吸引，数值越小越互相排斥
        .on("tick", tick)//指时间间隔，隔一段时间刷新一次画面
        .start();//开始转换

    var svg = d3.select("#network").append("svg")
        .attr("width", width)
        .attr("height", height);

    //箭头
    var marker=
        svg.append("marker")
        //.attr("id", function(d) { return d; })
            .attr("id", "resolved")
            //.attr("markerUnits","strokeWidth")//设置为strokeWidth箭头会随着线的粗细发生变化
            .attr("markerUnits","userSpaceOnUse")
            .attr("viewBox", "0 -5 10 10")//坐标系的区域
            .attr("refX",32)//箭头坐标
            .attr("refY", -1)
            .attr("markerWidth", 12)//标识的大小
            .attr("markerHeight", 12)
            .attr("orient", "auto")//绘制方向，可设定为：auto（自动确认方向）和 角度值
            .attr("stroke-width",2)//箭头宽度
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")//箭头的路径
            .attr('fill','#000000');//箭头颜色

    //    将连接线设置为曲线

    //设置连接线
    var edges_line = svg.selectAll(".edgepath")
        .data(force.links())
        .enter()
        .append("path")
        .attr({
            'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
            'class':'edgepath',
            //'fill-opacity':0,
            //'stroke-opacity':0,
            //'fill':'blue',
            //'stroke':'red',
            'id':function(d,i) {return 'edgepath'+i;}})
        .style("stroke",function(d){
            var lineColor;
            //根据关系的不同设置线条颜色
            if(d.type2=="enent_id"){
                lineColor="#9c27b0";
            }else if(d.type2=="uid"){
                lineColor="#2b2082";
            }else{
                lineColor="#e62144";
            }
            return lineColor;
        })
        .style("pointer-events", "none")
        .style("stroke-width",1.5)//线条粗细
        .attr("marker-end", "url(#resolved)" );//根据箭头标记的id号标记箭头

    var edges_text = svg.append("g").selectAll(".edgelabel")
        .data(force.links())
        .enter()
        .append("text")
        .style("pointer-events", "none")
        //.attr("class","linetext")
        .attr({
            'class':'edgelabel',
            'id':function(d,i){return 'edgepath'+i;},
            'dx':80,
            'dy':0
            //'font-size':10,
            //'fill':'#aaa'
        });

    //设置线条上的文字
    edges_text.append('textPath')
        .attr('xlink:href',function(d,i) {return '#edgepath'+i})
        .style("pointer-events", "none")
        .text(function(d){return d.type1;});

    //圆圈
    var circle = svg.append("g").selectAll("circle")
        .data(force.nodes())//表示使用force.nodes数据
        .enter().append("circle")
        .style("fill",function(node){
            var color;//圆圈背景色
            // var link=links[node.index];
            if(node.type2=="enent_id"){
                color="#F6E8E9";
            }else if(node.type2=="uid"){
                color="rgb(243, 25, 47)";
            }else{
                color="#00d464";
            }
            return color;
        })
        .style('stroke',function(node){
            var color;//圆圈线条的颜色
            // var link=links[node.index];
            if(node.type2=="enent_id"){
                color="#673ab7";
            }else if(node.type2=="uid"){
                color="#03A9F4";
            }else{
                color="#e91e63";
            }
            return color;
        })
        .attr("r", 28)//设置圆圈半径
        .on("click",function(node){
            //单击时让连接线加粗
            edges_line.style("stroke-width",function(line){
                if(line.source.name==node.name || line.target.name==node.name){
                    return 4;
                }else{
                    return 1.5;
                }
            });
            //d3.select(this).style('stroke-width',2);
        })
        //双击跳转
        .on("dblclick",function(node){
            console.log(node)
        })
        .call(force.drag);//将当前选中的元素传到drag函数中，使顶点可以被拖动

    var text = svg.append("g").selectAll("text")
        .data(force.nodes())
        //返回缺失元素的占位对象（placeholder），指向绑定的数据中比选定元素集多出的一部分元素。
        .enter()
        .append("text")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")//在圆圈中加上数据
        .style('fill',function(node){
            var color;//文字颜色
            // var link=links[node.index];
            if(node.type2=="enent_id"){
                color="#F6E8E9";
            }else if(node.type2=="uid"){
                color="rgb(243, 25, 47)";
            }else{
                color="#00d464";
            }
            return color;
        }).attr('x',function(d){
            // console.log(d.name+"---"+ d.name.length);
            var re_en = /[a-zA-Z]+/g;
            //如果是全英文，不换行
            if(d.name.match(re_en)){
                d3.select(this).append('tspan')
                    .attr('x',0)
                    .attr('y',2)
                    .text(function(){return d.name;});
            }
            //如果小于四个字符，不换行
            else if(d.name.length<=4){
                d3.select(this).append('tspan')
                    .attr('x',0)
                    .attr('y',2)
                    .text(function(){return d.name;});
            }else{
                var top=d.name.substring(0,4);
                var bot=d.name.substring(4,d.name.length);

                d3.select(this).text(function(){return '';});

                d3.select(this).append('tspan')
                    .attr('x',0)
                    .attr('y',-7)
                    .text(function(){return top;});

                d3.select(this).append('tspan')
                    .attr('x',0)
                    .attr('y',10)
                    .text(function(){return bot;});
            }
            //直接显示文字
            /*.text(function(d) {
             return d.name; */
        });


    function tick() {
        //path.attr("d", linkArc);//连接线
        circle.attr("transform", transform1);//圆圈
        text.attr("transform", transform2);//顶点文字
        //edges_text.attr("transform", transform3);
        //text2.attr("d", linkArc);//连接线文字
        //console.log("text2...................");
        //console.log(text2);
        //edges_line.attr("x1",function(d){ return d.source.x; });
        //edges_line.attr("y1",function(d){ return d.source.y; });
        //edges_line.attr("x2",function(d){ return d.target.x; });
        //edges_line.attr("y2",function(d){ return d.target.y; });

        //edges_line.attr("x",function(d){ return (d.source.x + d.target.x) / 2 ; });
        //edges_line.attr("y",function(d){ return (d.source.y + d.target.y) / 2 ; });


        edges_line.attr('d', function(d) {
            var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
            return path;
        });

        edges_text.attr('transform',function(d,i){
            if (d.target.x<d.source.x){
                bbox = this.getBBox();
                rx = bbox.x+bbox.width/2;
                ry = bbox.y+bbox.height/2;
                return 'rotate(180 '+rx+' '+ry+')';
            }
            else {
                return 'rotate(0)';
            }
        });
    }

    //设置连接线的坐标,使用椭圆弧路径段双向编码
    function linkArc(d) {
        //var dx = d.target.x - d.source.x,
        // dy = d.target.y - d.source.y,
        // dr = Math.sqrt(dx * dx + dy * dy);
        //return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
        //打点path格式是：Msource.x,source.yArr00,1target.x,target.y

        return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y
    }
    //设置圆圈和文字的坐标
    function transform1(d) {
        return "translate(" + d.x + "," + d.y + ")";
    }
    function transform2(d) {
        return "translate(" + (d.x) + "," + d.y + ")";
    }

}

//相关人物
function person(p_data) {
    var p_data = eval(p_data);
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
        showToggle:true,
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
                        return '无相似计算任务'+'<br/><a onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var go=row.uid+',User';
                        return '<a onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
            }
        }
    });
};

//相关机构
function agencies(data) {
    var data = eval(data);
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
        showToggle:true,
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
                        var infor=row.uname+','+row.id+',Org';
                        return '无相似计算任务'+'<br/><a onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var go=row.id+',Org';
                        return '<a onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
            }
        }
    });
};

//相关事件
function events(e_data) {
    var e_data = eval(e_data);
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
                    }else {
                        return row.event_type;
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
                        return '无相似计算任务'+'<br/><a onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var go=row.id+',Event';
                        return '<a onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
            }
        }
    });
};

//相关群体
function organization(data) {
    var data = eval(data);
    $('#organization').bootstrapTable('load', data);
    $('#organization').bootstrapTable({
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
                title: "组织名称",//标题
                field: "group_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'||row.group_name.length==0){
                        return row.id;
                    }else {
                        return row.group_name[0];
                    }
                }
            },
            {
                title: "关键词",//标题
                field: "k_label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var key='';
                        var words=value.split('&');
                        for (var k=0;k<words.length;k++){
                            key+=words[k]+' ';
                        }
                        return key;
                    }
                }
            },
            {
                title: "业务标签",//标题
                field: "label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=row.label.split('&');
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
                        return '无相似计算任务'+'<br/><a onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var go=row.id+',Group';
                        return '<a onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
            }
        }
    });
};

//相关专题
function subject(data) {
    var data = eval(data);
    $('#subject').bootstrapTable('load', data);
    $('#subject').bootstrapTable({
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
                title: "专题名称",//标题
                field: "event",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "关键词",//标题
                field: "k_label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=row.k_label.split('&');
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
                field: "label",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (value==''||value=='unknown'||value=='NULL'){
                        return '暂无';
                    }else {
                        var words=row.label.split('&');
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
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row.topic_name.length;
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
                        var infor=row.event+','+row.id+',SpecialEvent';
                        return '无相似计算任务'+'<br/><a onclick="add_new_task(\''+ infor +'\')">添加相似任务</a>';
                    }else if (value==0){
                        return '尚未计算';
                    }else if (value==1){
                        var go=row[1].uid+',SpecialEvent';
                        return '<a onclick="go_jump(\''+ go +'\')">计算完成</a>';
                    }else if (value==-1){
                        return '正在计算';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='尚未计算'||$element[0].innerText=='正在计算') {
                alert('还未计算完成。')
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
            var data=eval(data)
            console.log(data)
            if (data=='yes'){
                alert('创建成功。');
            }else {
                alert('创建失败。');
            }
        }
    });
}

function go_jump(uid_type) {
    var news=uid_type.split(',');
    window.open('/relation/similarity_result/?node_id='+news[0]+'&node_type='+news[1]);
};

// setTimeout(function () {
//     localStorage.removeItem('temp');
// },60000);

