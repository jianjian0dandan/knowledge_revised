//时间戳转换
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().substr(0,10);
};
//------------
var ajax_method;
function hot_spot_found() {
    ajax_method='GET';
}
hot_spot_found.prototype= {
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
var final_time,text_type='1',sort='retweeted';
function hot_line(data) {
    $('#trend_line').empty();
    var line=eval(data);
    var date=[],num_1=[],num_2=[];
    for (var i=0;i<line.length;i++){
        date.push(getLocalTime(line[i].ts));
        num_1.push(line[i].origin);
        num_2.push(line[i].retweet);
    }
    final_time=Date.parse(new Date(date[date.length-1]))/1000;
    var myChart = echarts.init(document.getElementById('trend_line'));
    var option = {
        title: {
            // text: '折线图堆叠'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['原创','转发']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: date
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'原创',
                type:'line',
                data:num_1,
                smooth:true,
                itemStyle:{
                    normal:{
                        areaStyle:{type:'default'}
                    }
                },
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            },
            {
                name:'转发',
                type:'line',
                data:num_2,
                smooth:true,
                itemStyle:{
                    normal:{
                        areaStyle:{type:'default'}
                    }
                },
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            }
        ]
    };
    myChart.setOption(option);
    var weibo_url='/brust/show_weibo_list/?ts='+final_time+'&type='+text_type+'&sort='+sort;
    hot_spot_found.call_request(weibo_url,weibo);
    myChart.on('click',function (params) {
        if (params.seriesName=='原创'){
            text_type=1;
            var weibo_url='/brust/show_weibo_list/?ts='+final_time+'&type='+text_type+'&sort='+sort;
            hot_spot_found.call_request(weibo_url,weibo);
        }else {
            text_type=3;
            var weibo_url='/brust/show_weibo_list/?ts='+final_time+'&type='+text_type+'&sort='+sort;
            hot_spot_found.call_request(weibo_url,weibo);
        }
    })
};
function weibo(data) {
    var data=eval(data);
    $('#menu-collapse').empty();
    var weibo_str='';
    for (var w=0;w<data.length;w++){
        var name,time,photo,text,key_words='';
        if(data[w].nick_name==''||data[w].nick_name=='unknown'
            ||data[w].nick_name=='null'||data[w].nick_name== undefined ){
            name=data[w].uid;
        }else {
            name=data[w].nick_name;
        };
        if(data[w].timestamp==''||data[w].timestamp=='unknown'
            ||data[w].timestamp=='null'||data[w].timestamp== undefined){
            time='暂无';
        }else {
            time=getLocalTime(data[w].timestamp);
        };
        if(data[w].photo_url==''||data[w].photo_url=='unknown'
            ||data[w].photo_url== undefined ||data[w].photo_url=='null'){
            photo='/static/images/unknown.png';
        }else {
            photo=data[w].photo_url;
        };
        if(data[w].text==''||data[w].text=='unknown'
            ||data[w].text=='null'||data[w].text== undefined){
            text='暂无';
        }else {
            text=data[w].text;
        };
        if(data[w].keywords_string==''||data[w].keywords_string=='unknown'
            ||data[w].keywords_string=='null'||data[w].keywords_string== undefined){
            key_words='暂无';
        }else {
            var word=data[w].keywords_string.split('&');
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
            '<div class="weibo">'+
            '     <h3>'+
            '         <span id="mid" style="display: none">'+data[w].mid+'</span>'+
            '         <span>热点'+(w+1)+'：</span>'+
            '         <a href="###" class="user_name">'+name+'</a>&nbsp;'+
            '         <span>于</span>'+
            '         <b class="time">'+time+'</b>&nbsp;'+
            '         <span>发布</span>'+
            '     </h3>'+
            '     <div class="content">'+
            '         <div class="content-1">'+
            '  				<img src="'+photo+'" alt="">'+
            '         </div>'+
            '         <div class="content-2">'+
            '  				<span class="speech">'+ text+'</span>'+
            '  				<p class="fd_nums">'+
            '      				<span>转发数:</span><b class="f_amount">'+data[w].retweeted+'</b>'+
            '      				<span>评论数:</span><b class="d_amount">'+data[w].comment+'</b>'+
            '  				</p>'+
            '  				<div class="content-3">'+
            '      				<span>关键词：</span>'+key_words+
            '      				<button class="judgment">热点研判</button>'+
            '  				</div>'+
            '         </div>'+
            '     </div>'+
            ' </div>';
    };
    $('#menu-collapse').append(weibo_str);
    $('.judgment').on('click',function () {
        var mid=$(this).parents('.weibo').find('#mid').text();
        window.open('/brust/result/?mid='+mid);
    })
    $("#menu-collapse").accordion();
}

//排序
$('#container .hot_find .sorting input').on('click',function () {
    sort=$(this).val();
    var weibo_url='/brust/show_weibo_list/?ts='+final_time+'&type='+text_type+'&sort='+sort;
    hot_spot_found.call_request(weibo_url,weibo);
});


var hot_spot_found=new hot_spot_found();
function hot() {
    var url = '/brust/show_weibo/';
    hot_spot_found.call_request(url,hot_line);
}
hot();