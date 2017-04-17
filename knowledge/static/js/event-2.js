var emtion={
    '0':'中性','1':'积极','2':'生气','3':'焦虑',
    '4':'悲伤','5':'厌恶','6':'消极其他',
};
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月|\//g, "-").replace(/日|上午|下午/g, " ").substr(0,10);
}
// 情绪走势图---折线图
var sentiment=result_1.sentiment_results[0];
var time=[];
var series=[];
var emtion0=[],emtion1=[],emtion2=[],emtion3=[],emtion4=[]
    ,emtion5=[],emtion6=[],emtion7=[];
$.each(sentiment,function (index,item) {
    time.push(getLocalTime(item[0]));
    for (var s in item[1]){
        if (s==0){
            emtion0.push(item[1][s]);
        }else if(s==1){
            emtion1.push(item[1][s]);
        }else if(s==2){
            emtion2.push(item[1][s]);
        }else if(s==3){
            emtion3.push(item[1][s]);
        }else if(s==4){
            emtion4.push(item[1][s]);
        }else if(s==5){
            emtion5.push(item[1][s]);
        }else if(s==6){
            emtion6.push(item[1][s]);
        }
    };

})
var myChart = echarts.init(document.getElementById('hot_trend'));
option = {
    title : {
        text: '情绪曲线图',
        left:'center',
        top:'5%'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['中性','积极','生气','焦虑','悲伤','厌恶','消极其他'],
        top:'0%',
        right:'5%'
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : time
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'中性',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:emtion0
        },
        {
            name:'积极',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:emtion1
        },
        {
            name:'生气',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:emtion2
        },
        {
            name:'焦虑',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:emtion3
        },
        {
            name:'悲伤',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:emtion4
        },
        {
            name:'厌恶',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:emtion5
        },
        {
            name:'消极其他',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:emtion6
        },
    ]
};
myChart.setOption(option);

// 地域走势图---地图
// var myChart = echarts.init(document.getElementById('place_trend'));
function randomData() {
    return Math.round(Math.random()*1000);
}
option = {
    title: {
        text: '地域统计图',
        left:'center'
    },
    tooltip: {
        trigger: 'item',
    },
    visualMap: {
        min: 0,
        max: 2500,
        left: 'left',
        top: 'bottom',
        itemWidth: 20,
        itemHeight: 80,
        text: ['高','低'],           // 文本，默认为数值文本
        inRange: {
            color: ['#e0ffff', '#006edd']
        },
        textStyle: {
            color: '#8e8e8e',
            fontSize: 12,
        },
        calculable: true
    },
    series: [
        {
            name:'地理位置',
            type: 'map',
            mapType: 'china',
            roam: true,
            layoutCenter:  ['50%', '50%'],
            layoutSize: 520,
            label: {
                normal: {
                    show: false,
                    areaColor: '#142d41',
                    borderColor: '#477bc4'
                },
                emphasis: {
                    show: true,
                    areaColor: '#67b4d0'
                }
            },
            data:[
                {name: '北京',value: 231 },
                {name: '天津',value: 56 },
                {name: '上海',value: 465 },
                {name: '广东',value: 345 },
                {name: '台湾',value: 56 },
                {name: '香港',value: 67 },
                {name: '澳门',value: 89 }
            ]
        }
    ]
};
// myChart.setOption(option);



require.config({
    paths: {
        echarts: '/static/js/echarts-2/build/dist',
    }
});
//--话题---
function createRandomItemStyle() {
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')'
        }
    };
};

var topics=result_1.topics;
var topics_list='';
$.each(topics,function (index,item) {
    topics_list+='<p><b>话题'+(index+1)+'：</b><span>'+item+'</span></p>';
});
$('#topic_trend').html(topics_list);



// 情绪走势图---折线图
var weibo_type={'1':'原创','2':'转发','3':'评论'};
var thing_hot=result_1.time_results[0];
var weibo_date=[];
var weibo1=[],weibo2=[],weibo3=[];
$.each(thing_hot,function (index,item) {
    weibo_date.push(getLocalTime(item[0]));
    for (var w in item[1]){
        if (w==1){
            weibo1.push(item[1][w]);
        }else if (w==2){
            weibo2.push(item[1][w]);
        }else if (w==3){
            weibo3.push(item[1][w]);
        }
    }
});
var myChart = echarts.init(document.getElementById('mood_trend'));
var option = {
    title: {
        text: '事件热度走势图',
        left:'center',
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data:['原创','转发','评论'],
        top:'10%',
        left:'center'
    },
    xAxis:  {
        type: 'category',
        boundaryGap: false,
        data:weibo_date
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            formatter: '{value} °C'
        }
    },
    series: [
        {
            name:'原创',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:weibo1
        },
        {
            name:'转发',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:weibo2
        },
        {
            name:'评论',
            type:'line',
            smooth:true,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data:weibo3
        },
    ]
};
myChart.setOption(option);

//参与讨论的人
var user=[];
// user.push(result_1.user_results);
for (var u in result_1.user_results){
    result_1.user_results[u]['uid']=u;
    user.push(result_1.user_results[u]);
}
function mood_trend(data) {
    $('#collection').bootstrapTable('load', data);
    $('#collection').bootstrapTable({
        data:data,
        search: false,//是否搜索
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
                title: "参与者uid",//标题
                field: "uid",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "参与者影响力",//标题
                field: "influ",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return row.influ.toFixed(2);
                }
            },
            {
                title: "参与者身份",//标题
                field: "user_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.user_type=='user'){
                        return '人物';
                    }else if (row.user_type=='auth'){
                        return '机构';
                    }
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if (field=='uid') {
                if (row.user_type=='user'){
                    window.open('/index/person/?user_id='+row.uid);
                }else {
                    window.open('/index/organization/?user_id='+row.uid);
                };
            }
        }
    });
};
mood_trend(user);

//微博讨论
function weibo(data){
    $('#group_emotion_loading').css('display', 'none');
    $('#input-table').css('display', 'block');
    var dataArray = data;
    var PageNo=document.getElementById('PageNo');                   //设置每页显示行数
    var InTb=document.getElementById('input-table');               //表格
    var Fp=document.getElementById('F-page');                      //首页
    var Nep=document.getElementById('Nex-page');                  //下一页
    var Prp=document.getElementById('Pre-page');                  //上一页
    var Lp=document.getElementById('L-page');                     //尾页
    var S1=document.getElementById('s1');                         //总页数
    var S2=document.getElementById('s2');                         //当前页数
    var currentPage;                                              //定义变量表示当前页数
    var SumPage;

    if(PageNo.value!="")                                       //判断每页显示是否为空
    {
        InTb.innerHTML='';                                     //每次进来都清空表格
        S2.innerHTML='';                                        //每次进来清空当前页数
        currentPage=1;                                          //首页为1
        S2.appendChild(document.createTextNode(currentPage));
        S1.innerHTML='';                                        //每次进来清空总页数
        if(dataArray.length%PageNo.value==0)                    //判断总的页数
        {
            SumPage=parseInt(dataArray.length/PageNo.value);
        }
        else
        {
            SumPage=parseInt(dataArray.length/PageNo.value)+1
        }
        S1.appendChild(document.createTextNode(SumPage));
        var oTBody=document.createElement('tbody');               //创建tbody
        oTBody.setAttribute('class','In-table');                   //定义class
        InTb.appendChild(oTBody);                                     //将创建的tbody添加入table
        var html_c = '';

        if(dataArray==''){
            html_c = "<p style='text-align: center'>用户未发布任何微博</p>";
            oTBody.innerHTML = html_c;
        }else{

            for(i=0;i<parseInt(PageNo.value);i++)
            {                                                          //循环打印数组值
                oTBody.insertRow(i);
                var name,text,time;
                if (dataArray[i].name==''||dataArray[i].name=='unknown') {
                    name=dataArray[i].uid;
                }else {
                    name=dataArray[i].name;
                };
                if (dataArray[i].time==''||dataArray[i].time=='unknown') {
                    time='未知';
                }else {
                    time=dataArray[i].time;
                };
                if (dataArray[i].text==''||dataArray[i].text=='unknown') {
                    text='未发表任何内容';
                }else {
                    text=dataArray[i].text;
                };
                html_c =
                    '<div class="published">'+
                    '     <span id="'+data[i].mid+'"></span>'+
                    '     <p class="master">'+
                    '          微博内容：'+
                    '          <span class="master1">'+text+'</span>'+
                    '     </p>'+
                    '     <p class="time">'+
                    '        <span class="time1">来自微博用户：</span>&nbsp;'+
                    '        <a href='+'"http://www.weibo.com/u/'+dataArray[i].uid+'"'+' class="time2">'+name+'</a>&nbsp;&nbsp;'+
                    '        <span class="time3">发表于&nbsp;<i>'+time+'</i></span>'+
                    '        <span style="display: inline-block;float:right;">'+
                    '        <span class="time4">转发数（'+dataArray[i].retweeted+'）</span>|&nbsp;'+
                    '        <span class="time5">评论数（'+dataArray[i].comment+'）</span></span>'+
                    '     </p>'+
                    '</div>';
                oTBody.rows[i].insertCell(0);
                oTBody.rows[i].cells[0].innerHTML = html_c;
            }
        }
    }

    Fp.onclick=function()
    {

        if(PageNo.value!="")                                       //判断每页显示是否为空
        {
            InTb.innerHTML='';                                     //每次进来都清空表格
            S2.innerHTML='';                                        //每次进来清空当前页数
            currentPage=1;                                          //首页为1
            S2.appendChild(document.createTextNode(currentPage));
            S1.innerHTML='';                                        //每次进来清空总页数
            if(dataArray.length%PageNo.value==0)                    //判断总的页数
            {
                SumPage=parseInt(dataArray.length/PageNo.value);
            }
            else
            {
                SumPage=parseInt(dataArray.length/PageNo.value)+1
            }
            S1.appendChild(document.createTextNode(SumPage));
            var oTBody=document.createElement('tbody');               //创建tbody
            oTBody.setAttribute('class','In-table');                   //定义class
            InTb.appendChild(oTBody);                                     //将创建的tbody添加入table
            var html_c = '';

            if(dataArray==''){
                html_c = "<p style='width:840px;text-align: center'>用户未发布任何微博</p>";
                oTBody.innerHTML = html_c;
            }else{

                for(i=0;i<parseInt(PageNo.value);i++)
                {                                                          //循环打印数组值
                    oTBody.insertRow(i);
                    var name,text,time;
                    if (dataArray[i].name==''||dataArray[i].name=='unknown') {
                        name=dataArray[i].uid;
                    }else {
                        name=dataArray[i].name;
                    };
                    if (dataArray[i].time==''||dataArray[i].time=='unknown') {
                        time='未知';
                    }else {
                        time=dataArray[i].time;
                    };
                    if (dataArray[i].text==''||dataArray[i].text=='unknown') {
                        text='未发表任何内容';
                    }else {
                        text=dataArray[i].text;
                    };
                    html_c =
                        '<div class="published">'+
                        '     <span id="'+dataArray[i].mid+'"></span>'+
                        '     <p class="master">'+
                        '          微博内容：'+
                        '          <span class="master1">'+text+'</span>'+
                        '     </p>'+
                        '     <p class="time">'+
                        '        <span class="time1">来自微博用户：</span>&nbsp;'+
                        '        <a href='+'"http://www.weibo.com/u/'+dataArray[i].uid+'"'+' class="time2">'+name+'</a>&nbsp;&nbsp;'+
                        '        <span class="time3">发表于&nbsp;<i>'+time+'</i></span>'+
                        '        <span style="display: inline-block;float:right;">'+
                        '        <span class="time4">转发数（'+dataArray[i].retweeted+'）</span>|&nbsp;'+
                        '        <span class="time5">评论数（'+dataArray[i].comment+'）</span></span>'+
                        '     </p>'+
                        '</div>';
                    oTBody.rows[i].insertCell(0);
                    oTBody.rows[i].cells[0].innerHTML = html_c;
                }
            }
        }
    }

    Nep.onclick=function()
    {
        if(currentPage<SumPage)                                 //判断当前页数小于总页数
        {
            InTb.innerHTML='';
            S1.innerHTML='';
            if(dataArray.length%PageNo.value==0)
            {
                SumPage=parseInt(dataArray.length/PageNo.value);
            }
            else
            {
                SumPage=parseInt(dataArray.length/PageNo.value)+1
            }
            S1.appendChild(document.createTextNode(SumPage));
            S2.innerHTML='';
            currentPage=currentPage+1;
            S2.appendChild(document.createTextNode(currentPage));
            var oTBody=document.createElement('tbody');
            oTBody.setAttribute('class','In-table');
            InTb.appendChild(oTBody);
            var a;                                                 //定义变量a
            a=PageNo.value*(currentPage-1);                       //a等于每页显示的行数乘以上一页数
            var c;                                                  //定义变量c
            if(dataArray.length-a>=PageNo.value)                  //判断下一页数组数据是否小于每页显示行数
            {
                c=PageNo.value;
            }
            else
            {
                c=dataArray.length-a;
            }
            for(i=0;i<c;i++)
            {
                oTBody.insertRow(i);
                var name,text,time;
                if (dataArray[i+a].name==''||dataArray[i+a].name=='unknown') {
                    name=dataArray[i+a].uid;
                }else {
                    name=dataArray[i+a].name;
                };
                if (dataArray[i+a].time==''||dataArray[i+a].time=='unknown') {
                    time='未知';
                }else {
                    time=dataArray[i+a].time;
                };
                if (dataArray[i+a].text==''||dataArray[i+a].text=='unknown') {
                    text='未发表任何内容';
                }else {
                    text=dataArray[i+a].text;
                };
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="published">'+
                    '     <span id="'+dataArray[i+a].mid+'"></span>'+
                    '     <p class="master">'+
                    '          微博内容：'+
                    '          <span class="master1">'+text+'</span>'+
                    '     </p>'+
                    '     <p class="time">'+
                    '        <span class="time1">来自微博用户：</span>&nbsp;'+
                    '        <a href='+'"http://www.weibo.com/u/'+dataArray[i+a].uid+'"'+' class="time2">'+name+'</a>&nbsp;&nbsp;'+
                    '        <span class="time3">发表于&nbsp;<i>'+time+'</i></span>'+
                    '        <span style="display: inline-block;float:right;">'+
                    '        <span class="time4">转发数（'+dataArray[i+a].retweeted+'）</span>|&nbsp;'+
                    '        <span class="time5">评论数（'+dataArray[i+a].comment+'）</span></span>'+
                    '     </p>'+
                    '</div>';
                oTBody.rows[i].cells[0].innerHTML = html_c;
                //数组从第i+a开始取值
            }
        }
    }

    Prp.onclick=function()
    {
        if(currentPage>1)                        //判断当前是否在第一页
        {
            InTb.innerHTML='';
            S1.innerHTML='';
            if(dataArray.length%PageNo.value==0)
            {
                SumPage=parseInt(dataArray.length/PageNo.value);
            }
            else
            {
                SumPage=parseInt(dataArray.length/PageNo.value)+1
            }
            S1.appendChild(document.createTextNode(SumPage));
            S2.innerHTML='';
            currentPage=currentPage-1;
            S2.appendChild(document.createTextNode(currentPage));
            var oTBody=document.createElement('tbody');
            oTBody.setAttribute('class','In-table');
            InTb.appendChild(oTBody);
            var a;
            a=PageNo.value*(currentPage-1);
            for(i=0;i<parseInt(PageNo.value);i++)
            {
                oTBody.insertRow(i);
                var name,text,time;
                if (dataArray[i+a].name==''||dataArray[i+a].name=='unknown') {
                    name=dataArray[i+a].uid;
                }else {
                    name=dataArray[i+a].name;
                };
                if (dataArray[i+a].time==''||dataArray[i+a].time=='unknown') {
                    time='未知';
                }else {
                    time=dataArray[i+a].time;
                };
                if (dataArray[i+a].text==''||dataArray[i+a].text=='unknown') {
                    text='未发表任何内容';
                }else {
                    text=dataArray[i+a].text;
                };
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="published">'+
                    '     <span id="'+dataArray[i+a].mid+'"></span>'+
                    '     <p class="master">'+
                    '          微博内容：'+
                    '          <span class="master1">'+text+'</span>'+
                    '     </p>'+
                    '     <p class="time">'+
                    '        <span class="time1">来自微博用户：</span>&nbsp;'+
                    '        <a href='+'"http://www.weibo.com/u/'+dataArray[i+a].uid+'"'+' class="time2">'+name+'</a>&nbsp;&nbsp;'+
                    '        <span class="time3">发表于&nbsp;<i>'+time+'</i></span>'+
                    '        <span style="display: inline-block;float:right;">'+
                    '        <span class="time4">转发数（'+dataArray[i+a].retweeted+'）</span>|&nbsp;'+
                    '        <span class="time5">评论数（'+dataArray[i+a].comment+'）</span></span>'+
                    '     </p>'+
                    '</div>';
                oTBody.rows[i].cells[0].innerHTML = html_c;
            }
        }
    }

    Lp.onclick=function()
    {
        InTb.innerHTML='';
        S1.innerHTML='';
        if(dataArray.length%PageNo.value==0)
        {
            SumPage=parseInt(dataArray.length/PageNo.value);
        }
        else
        {
            SumPage=parseInt(dataArray.length/PageNo.value)+1
        }
        S1.appendChild(document.createTextNode(SumPage));
        S2.innerHTML='';
        currentPage=SumPage;
        S2.appendChild(document.createTextNode(currentPage));
        var oTBody=document.createElement('tbody');
        oTBody.setAttribute('class','In-table');
        InTb.appendChild(oTBody);
        var a;
        a=PageNo.value*(currentPage-1);
        var c;
        if(dataArray.length-a>=PageNo.value)
        {
            c=PageNo.value;
        }
        else
        {
            c=dataArray.length-a;
        }
        for(i=0;i<c;i++)
        {
            oTBody.insertRow(i);
            var name,text,time;
            if (dataArray[i+a].name==''||dataArray[i+a].name=='unknown') {
                name=dataArray[i+a].uid;
            }else {
                name=dataArray[i+a].name;
            };
            if (dataArray[i+a].time==''||dataArray[i+a].time=='unknown') {
                time='未知';
            }else {
                time=dataArray[i+a].time;
            };
            if (dataArray[i+a].text==''||dataArray[i+a].text=='unknown') {
                text='未发表任何内容';
            }else {
                text=dataArray[i+a].text;
            };
            oTBody.rows[i].insertCell(0);
            html_c =
                '<div class="published">'+
                '     <span id="'+dataArray[i+a].mid+'"></span>'+
                '     <p class="master">'+
                '          微博内容：'+
                '          <span class="master1">'+text+'</span>'+
                '     </p>'+
                '     <p class="time">'+
                '        <span class="time1">来自微博用户：</span>&nbsp;'+
                '        <a href='+'"http://www.weibo.com/u/'+dataArray[i+a].uid+'"'+' class="time2">'+name+'</a>&nbsp;&nbsp;'+
                '        <span class="time3">发表于&nbsp;<i>'+time+'</i></span>'+
                '        <span style="display: inline-block;float:right;">'+
                '        <span class="time4">转发数（'+dataArray[i+a].retweeted+'）</span>|&nbsp;'+
                '        <span class="time5">评论数（'+dataArray[i+a].comment+'）</span></span>'+
                '     </p>'+
                '</div>';
            oTBody.rows[i].cells[0].innerHTML = html_c;
        }
    }

}
weibo(result_3.all);
$('.text_info .button_list #all').on('click',function () {
    $(this).css({backgroundColor:'#337ab7'}).siblings('button').css({backgroundColor:'#02aacf'});
    $('#influeweibo #input-table .In-table').empty();
    weibo(result_3.all);
});
$('.text_info .button_list #media').on('click',function () {
    $(this).css({backgroundColor:'#337ab7'}).siblings('button').css({backgroundColor:'#02aacf'});
    $('#influeweibo #input-table .In-table').empty();
    weibo(result_3.media);
});
$('.text_info .button_list #internet_users').on('click',function () {
    $(this).css({backgroundColor:'#337ab7'}).siblings('button').css({backgroundColor:'#02aacf'});
    $('#influeweibo #input-table .In-table').empty();
    weibo(result_3.people);
});



