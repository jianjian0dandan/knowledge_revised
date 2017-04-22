//时间戳转换
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().substr(0,10);
};
//===
var ajax_method;
function sudden() {
    ajax_method='GET';
}
sudden.prototype= {
    call_request:function(url,callback) {
        $.ajax({
            url: url,
            type: ajax_method,
            dataType: 'json',
            async: true,
            success:callback
        });
    },
};

function current(data) {
    var data=eval(data);
    var weibo_str='';
    var name,time,photo,text,key_words='';
    if(data.nick_name==''||data.nick_name=='unknown'
        ||data.nick_name=='null'||data.nick_name== undefined ){
        name=data.uid;
    }else {
        name=data.nick_name;
    };
    if(data.timestamp==''||data.timestamp=='unknown'
        ||data.timestamp=='null'||data.timestamp== undefined){
        time='暂无';
    }else {
        time=getLocalTime(data.timestamp);
    };
    if(data.photo_url==''||data.photo_url=='unknown'
        ||data.photo_url== undefined ||data.photo_url=='null'){
        photo='/static/images/unknown.png';
    }else {
        photo=data.photo_url;
    };
    if(data.text==''||data.text=='unknown'
        ||data.text=='null'||data.text== undefined){
        text='暂无';
    }else {
        text=data.text;
    };
    if(data.keywords_string==''||data.keywords_string=='unknown'
        ||data.keywords_string=='null'||data.keywords_string== undefined){
        key_words='暂无';
    }else {
        var word=data.keywords_string.split('&');
        if (word.length>5){
            for (var kw=0;kw<5;kw++){
                key_words+='<a>'+word[kw]+'</a> ';
            }
        }else {
            for (var kw=0;kw<word.length;kw++){
                key_words+='<a>'+word[kw]+'</a> ';
            }
        }
    }
    weibo_str+=
        '<div class="weibo" style="padding:8px 10px;">'+
        '    <div class="user">'+
        '        <div class="user_left">'+
        '             <img src="'+photo+'" alt="">'+
        '        </div>'+
        '        <div class="user_right">'+
        '              <a href="###" class="user_name">'+name+'</a>&nbsp;<span>于</span>'+
        '              <b class="time">'+time+'</b>&nbsp;<span>发表：</span>'+
        '           <span class="speech">'+text+'</span>'+
        '           <p class="fd_nums">'+
        '               <span>转发数:</span><b class="f_amount">'+data.retweeted+'</b>'+
        '               <span>评论数:</span><b class="d_amount">'+data.comment+'</b>'+
        '           </p>'+
        '        </div>'+
        '    </div>'+
        '</div>';
    $('.weibo_content').append(weibo_str);
    $('.forecast_content .time').text(getLocalTime(data.detect_ts));
    $('.forecast_content .people').text(Math.round(data.uid_prediction));
    $('.forecast_content .weibo_count').text(Math.round(data.weibo_prediction));
    //画图
    var exist_time=[],exist_nums=[],
        rise_time=[],rise_nums=[],
        fall_time=[],fall_nums=[];
    for (var key in data.trendline){
        if (key=='exist_trend'){
            $.each(data.trendline[key],function (index,item) {
                exist_time.push(getLocalTime(item[0]));
                exist_nums.push(item[1]);
            })
        };
        if (key=='rise_trend'){
            $.each(data.trendline[key],function (index,item) {
                rise_time.push(getLocalTime(item[0]));
                rise_nums.push(item[1]);
            })
        };
        if (key=='fall_trend'){
            $.each(data.trendline[key],function (index,item) {
                fall_time.push(getLocalTime(item[0]));
                fall_nums.push(item[1]);
            })
        }
    };
    var a=exist_nums[exist_nums.length-1];
    fall_nums.unshift(a);
    var myChart = echarts.init(document.getElementById('forecast_img'));
    var time=[],series=[];
    for (var k=0;k<exist_nums.length;k++){
        rise_nums.unshift('');
    };
    if (!rise_nums==[]){
        for (var t=0;t<exist_nums.length-1;t++){
            fall_nums.unshift('');
        }
        $.each(exist_time,function (index,item) {
            time.push(item);
        })
        $.each(fall_time,function (index,item) {
            time.push(item);
        })
        series.push(
            {
                name:'趋势预测',
                type:'line',
                smooth:true,
                itemStyle: {
                    normal: {
                        color: '#1790cf',
                    }
                },
                areaStyle: {
                    normal: {
                        shadowColor:'#1790cf',
                    }
                },
                data:exist_nums,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
            },
            {
                name:'趋势走低',
                type:'line',
                lineStyle:{
                    normal:{
                        color: 'green',
                        type:'dotted'
                    }
                },
                data:fall_nums,
            }
        );
    }else {
        for (var t=0;t<(exist_nums.length+rise_nums.length-2);t++){
            fall_nums.unshift('');
        }
        $.each(exist_time,function (index,item) {
            time.push(item);
        })
        $.each(rise_time,function (index,item) {
            time.push(item);
        })
        $.each(fall_time,function (index,item) {
            time.push(item);
        })
        series.push(
            {
                name:'趋势预测',
                type:'line',
                smooth:true,
                itemStyle: {
                    normal: {
                        color: '#1790cf',
                    }
                },
                areaStyle: {
                    normal: {
                        shadowColor:'#1790cf',
                    }
                },
                data:exist_nums,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
                // markLine : {
                //     data : [
                //         {type : 'average', name: '平均值'}
                //     ]
                // }
            },
            {
                name:'趋势攀高',
                type:'line',
                lineStyle:{
                    normal:{
                        color: 'red',
                        type:'dotted'
                    }
                },
                data:rise_nums,
            },
            {
                name:'趋势走低',
                type:'line',
                lineStyle:{
                    normal:{
                        color: 'green',
                        type:'dotted'
                    }
                },
                data:fall_nums,
            }
        );
    }

    var option = {
        title : {
            // text: '某楼盘销售情况',
            // subtext: '纯属虚构'
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            // data:['欺诈电话']
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data: time,
                axisLabel: {
                    textStyle: {
                        color: 'black',
                        fontFamily: '微软雅黑',
                        fontSize: 14,
                    },
                }
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel: {
                    formatter: '{value} 次',
                    textStyle: {
                        color: 'black',
                        fontFamily: '微软雅黑',
                        fontSize: 14,
                    },
                }
            }
        ],
        series : series
    };
    // 为echarts对象加载数据
    myChart.setOption(option);

}


//===========================================
var sudden=new sudden();
function analysis() {
    var url = '/brust/show_weibo_bursting/?mid='+mid;
    sudden.call_request(url,current);
    var weibo_url = '/brust/show_current_hot_weibo/?mid='+mid;
    sudden.call_request(weibo_url,forward_discussion);
}
analysis();

function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日|上午|下午/g, " ");
}
// ===微博=========================
function forward_discussion(data){
    var data=eval(data);
    $('#weibo').empty();
    var weibo_str='';
    for (var w=0;w<data.hot_comment.length;w++){
        var name,time,photo,text;
        if(data.hot_comment[w].nick_name==''||data.hot_comment[w].nick_name=='unknown'
            ||data.hot_comment[w].nick_name=='null'||data.hot_comment[w].nick_name== undefined ){
            name=data.hot_comment[w].uid;
        }else {
            name=data.hot_comment[w].nick_name;
        };
        if(data.hot_comment[w].timestamp==''||data.hot_comment[w].timestamp=='unknown'
            ||data.hot_comment[w].timestamp=='null'||data.hot_comment[w].timestamp== undefined){
            time='暂无';
        }else {
            time=getLocalTime(data.hot_comment[w].timestamp);
        };
        if(data.hot_comment[w].photo_url==''||data.hot_comment[w].photo_url=='unknown'
            ||data.hot_comment[w].photo_url== undefined ||data.hot_comment[w].photo_url=='null'){
            photo='/static/images/unknown.png';
        }else {
            photo=data.hot_comment[w].photo_url;
        };
        if(data.hot_comment[w].text==''||data.hot_comment[w].text=='unknown'
            ||data.hot_comment[w].text=='null'||data.hot_comment[w].text== undefined){
            text='暂无';
        }else {
            text=data.hot_comment[w].text;
        };
        weibo_str+=
            '<div class="weibo" style="padding:8px 10px;">'+
            '    <div class="user">'+
            '        <div class="user_left">'+
            '             <img src="'+photo+'" alt="">'+
            '        </div>'+
            '        <div class="user_right">'+
            '           <a href="###" class="user_name">'+name+'</a>&nbsp;<span>于</span>'+
            '           <b class="time">'+time+'</b>&nbsp;<span>发表：</span>'+
            '           <span class="speech">'+text+'</span>'+
            '           <p class="fd_nums">'+
            '               <span>转发数:</span><b class="f_amount">'+data.hot_comment[w].retweeted+'</b>'+
            '               <span>评论数:</span><b class="d_amount">'+data.hot_comment[w].comment+'</b>'+
            '           </p>'+
            '        </div>'+
            '    </div>'+
            '</div>';
    };
    $('#weibo').append(weibo_str);
}

