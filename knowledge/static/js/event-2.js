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
    topics_list+='<p><b>话题'+item[0]+'：</b><span>'+item[1]+'</span></p>';
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
            if ($element[0].innerText=='查看专题') {
                window.open('/theme/result/?theme_name='+row[1]);
            }else if ($element[0].innerText=='编辑专题') {
                window.open('/theme/modify/?theme_name='+row[1]);
            }
        }
    });
};
mood_trend(user);




