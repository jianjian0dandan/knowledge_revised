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

function weibo(data){
    var data=eval(data);
    // $('#weibo_content').empty();
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

    if($(PageNo).val()!="")                                       //判断每页显示是否为空
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
                var name,time,photo,text,key_words='';
                if(dataArray[i].nick_name==''||dataArray[i].nick_name=='unknown'
                    ||dataArray[i].nick_name=='null'||dataArray[i].nick_name== undefined ){
                    name=dataArray[i].uid;
                }else {
                    name=dataArray[i].nick_name;
                };
                if(dataArray[i].timestamp==''||dataArray[i].timestamp=='unknown'
                    ||dataArray[i].timestamp=='null'||dataArray[i].timestamp== undefined){
                    time='暂无';
                }else {
                    time=getLocalTime(dataArray[i].timestamp);
                };
                if(dataArray[i].photo_url==''||dataArray[i].photo_url=='unknown'
                    ||dataArray[i].photo_url== undefined ||dataArray[i].photo_url=='null'){
                    photo='/static/images/unknown.png';
                }else {
                    photo=dataArray[i].photo_url;
                };
                if(dataArray[i].text==''||dataArray[i].text=='unknown'
                    ||dataArray[i].text=='null'||dataArray[i].text== undefined){
                    text='暂无';
                }else {
                    text=dataArray[i].text;
                };
                if(dataArray[i].keywords_string==''||dataArray[i].keywords_string=='unknown'
                    ||dataArray[i].keywords_string=='null'||dataArray[i].keywords_string== undefined){
                    key_words='暂无';
                }else {
                    var word=dataArray[i].keywords_string.split('&');
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
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="weibo">'+
                    '     <h3>'+
                    '         <span id="mid" style="display: none">'+dataArray[i].mid+'</span>'+
                    '         <span>热点'+(i+1)+'：</span>'+
                    '         <a href="###" class="user_name">'+name+'</a>&nbsp;'+
                    '         <span>于</span>'+
                    '         <b class="time">'+time+'</b>&nbsp;'+
                    '         <span>发布</span>'+
                    '     </h3>'+
                    '     <div class="content">'+
                    '         <div class="content-1">'+
                    '               <img src="'+photo+'" alt="">'+
                    '         </div>'+
                    '         <div class="content-2">'+
                    '               <span class="speech">'+ text+'</span>'+
                    '               <p class="fd_nums">'+
                    '                   <span>转发数:</span><b class="f_amount">'+dataArray[i].retweeted+'</b>'+
                    '                   <span>评论数:</span><b class="d_amount">'+dataArray[i].comment+'</b>'+
                    '               </p>'+
                    '               <div class="content-3">'+
                    '                   <span>关键词：</span>'+key_words+
                    '                   <button class="judgment">热点研判</button>'+
                    '               </div>'+
                    '         </div>'+
                    '     </div>'+
                    ' </div>';

                oTBody.rows[i].cells[0].innerHTML = html_c;
                // $('.judgment').on('click',function () {
                //     var mid=$(this).parents('.weibo').find('#mid').text();
                //     window.open('/brust/result/?mid='+mid);
                // })
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
                    var name,time,photo,text,key_words='';
                    if(dataArray[i].nick_name==''||dataArray[i].nick_name=='unknown'
                        ||dataArray[i].nick_name=='null'||dataArray[i].nick_name== undefined ){
                        name=dataArray[i].uid;
                    }else {
                        name=dataArray[i].nick_name;
                    };
                    if(dataArray[i].timestamp==''||dataArray[i].timestamp=='unknown'
                        ||dataArray[i].timestamp=='null'||dataArray[i].timestamp== undefined){
                        time='暂无';
                    }else {
                        time=getLocalTime(dataArray[i].timestamp);
                    };
                    if(dataArray[i].photo_url==''||dataArray[i].photo_url=='unknown'
                        ||dataArray[i].photo_url== undefined ||dataArray[i].photo_url=='null'){
                        photo='/static/images/unknown.png';
                    }else {
                        photo=dataArray[i].photo_url;
                    };
                    if(dataArray[i].text==''||dataArray[i].text=='unknown'
                        ||dataArray[i].text=='null'||dataArray[i].text== undefined){
                        text='暂无';
                    }else {
                        text=dataArray[i].text;
                    };
                    if(dataArray[i].keywords_string==''||dataArray[i].keywords_string=='unknown'
                        ||dataArray[i].keywords_string=='null'||dataArray[i].keywords_string== undefined){
                        key_words='暂无';
                    }else {
                        var word=dataArray[i].keywords_string.split('&');
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
                    html_c =
                        '<div class="weibo">'+
                        '     <h3>'+
                        '         <span id="mid" style="display: none">'+dataArray[i].mid+'</span>'+
                        '         <span>热点'+(i+1)+'：</span>'+
                        '         <a href="###" class="user_name">'+name+'</a>&nbsp;'+
                        '         <span>于</span>'+
                        '         <b class="time">'+time+'</b>&nbsp;'+
                        '         <span>发布</span>'+
                        '     </h3>'+
                        '     <div class="content">'+
                        '         <div class="content-1">'+
                        '               <img src="'+photo+'" alt="">'+
                        '         </div>'+
                        '         <div class="content-2">'+
                        '               <span class="speech">'+ text+'</span>'+
                        '               <p class="fd_nums">'+
                        '                   <span>转发数:</span><b class="f_amount">'+dataArray[i].retweeted+'</b>'+
                        '                   <span>评论数:</span><b class="d_amount">'+dataArray[i].comment+'</b>'+
                        '               </p>'+
                        '               <div class="content-3">'+
                        '                   <span>关键词：</span>'+key_words+
                        '                   <button class="judgment">热点研判</button>'+
                        '               </div>'+
                        '         </div>'+
                        '     </div>'+
                        ' </div>';
                    oTBody.rows[i].insertCell(0);
                    oTBody.rows[i].cells[0].innerHTML = html_c;
                    // $('.judgment').on('click',function () {
                    //     var mid=$(this).parents('.weibo').find('#mid').text();
                    //     window.open('/brust/result/?mid='+mid);
                    // })
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
                var name,time,photo,text,key_words='';
                if(data[i+a].nick_name==''||data[i+a].nick_name=='unknown'
                    ||data[i+a].nick_name=='null'||data[i+a].nick_name== undefined ){
                    name=data[i+a].uid;
                }else {
                    name=data[i+a].nick_name;
                };
                if(data[i+a].timestamp==''||data[i+a].timestamp=='unknown'
                    ||data[i+a].timestamp=='null'||data[i+a].timestamp== undefined){
                    time='暂无';
                }else {
                    time=getLocalTime(data[i+a].timestamp);
                };
                if(data[i+a].photo_url==''||data[i+a].photo_url=='unknown'
                    ||data[i+a].photo_url== undefined ||data[i+a].photo_url=='null'){
                    photo='/static/images/unknown.png';
                }else {
                    photo=data[i+a].photo_url;
                };
                if(data[i+a].text==''||data[i+a].text=='unknown'
                    ||data[i+a].text=='null'||data[i+a].text== undefined){
                    text='暂无';
                }else {
                    text=data[i+a].text;
                };
                if(data[i+a].keywords_string==''||data[i+a].keywords_string=='unknown'
                    ||data[i+a].keywords_string=='null'||data[i+a].keywords_string== undefined){
                    key_words='暂无';
                }else {
                    var word=data[i+a].keywords_string.split('&');
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
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="weibo">'+
                    '     <h3>'+
                    '         <span id="mid" style="display: none">'+data[i+a].mid+'</span>'+
                    '         <span>热点'+(i+a+1)+'：</span>'+
                    '         <a href="###" class="user_name">'+name+'</a>&nbsp;'+
                    '         <span>于</span>'+
                    '         <b class="time">'+time+'</b>&nbsp;'+
                    '         <span>发布</span>'+
                    '     </h3>'+
                    '     <div class="content">'+
                    '         <div class="content-1">'+
                    '               <img src="'+photo+'" alt="">'+
                    '         </div>'+
                    '         <div class="content-2">'+
                    '               <span class="speech">'+ text+'</span>'+
                    '               <p class="fd_nums">'+
                    '                   <span>转发数:</span><b class="f_amount">'+data[i+a].retweeted+'</b>'+
                    '                   <span>评论数:</span><b class="d_amount">'+data[i+a].comment+'</b>'+
                    '               </p>'+
                    '               <div class="content-3">'+
                    '                   <span>关键词：</span>'+key_words+
                    '                   <button class="judgment">热点研判</button>'+
                    '               </div>'+
                    '         </div>'+
                    '     </div>'+
                    ' </div>';
                oTBody.rows[i].cells[0].innerHTML = html_c;
                //数组从第i+a开始取值
                // $('.judgment').on('click',function () {
                //     var mid=$(this).parents('.weibo').find('#mid').text();
                //     window.open('/brust/result/?mid='+mid);
                // })
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
                var name,time,photo,text,key_words='';
                if(data[i+a].nick_name==''||data[i+a].nick_name=='unknown'
                    ||data[i+a].nick_name=='null'||data[i+a].nick_name== undefined ){
                    name=data[i+a].uid;
                }else {
                    name=data[i+a].nick_name;
                };
                if(data[i+a].timestamp==''||data[i+a].timestamp=='unknown'
                    ||data[i+a].timestamp=='null'||data[i+a].timestamp== undefined){
                    time='暂无';
                }else {
                    time=getLocalTime(data[i+a].timestamp);
                };
                if(data[i+a].photo_url==''||data[i+a].photo_url=='unknown'
                    ||data[i+a].photo_url== undefined ||data[i+a].photo_url=='null'){
                    photo='/static/images/unknown.png';
                }else {
                    photo=data[i+a].photo_url;
                };
                if(data[i+a].text==''||data[i+a].text=='unknown'
                    ||data[i+a].text=='null'||data[i+a].text== undefined){
                    text='暂无';
                }else {
                    text=data[i+a].text;
                };
                if(data[i+a].keywords_string==''||data[i+a].keywords_string=='unknown'
                    ||data[i+a].keywords_string=='null'||data[i+a].keywords_string== undefined){
                    key_words='暂无';
                }else {
                    var word=data[i+a].keywords_string.split('&');
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
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="weibo">'+
                    '     <h3>'+
                    '         <span id="mid" style="display: none">'+data[i+a].mid+'</span>'+
                    '         <span>热点'+(i+a+1)+'：</span>'+
                    '         <a href="###" class="user_name">'+name+'</a>&nbsp;'+
                    '         <span>于</span>'+
                    '         <b class="time">'+time+'</b>&nbsp;'+
                    '         <span>发布</span>'+
                    '     </h3>'+
                    '     <div class="content">'+
                    '         <div class="content-1">'+
                    '               <img src="'+photo+'" alt="">'+
                    '         </div>'+
                    '         <div class="content-2">'+
                    '               <span class="speech">'+ text+'</span>'+
                    '               <p class="fd_nums">'+
                    '                   <span>转发数:</span><b class="f_amount">'+data[i+a].retweeted+'</b>'+
                    '                   <span>评论数:</span><b class="d_amount">'+data[i+a].comment+'</b>'+
                    '               </p>'+
                    '               <div class="content-3">'+
                    '                   <span>关键词：</span>'+key_words+
                    '                   <button class="judgment">热点研判</button>'+
                    '               </div>'+
                    '         </div>'+
                    '     </div>'+
                    ' </div>';
                oTBody.rows[i].cells[0].innerHTML = html_c;
                // $('.judgment').on('click',function () {
                //     var mid=$(this).parents('.weibo').find('#mid').text();
                //     window.open('/brust/result/?mid='+mid);
                // })
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
            var name,time,photo,text,key_words='';
            if(data[i+a].nick_name==''||data[i+a].nick_name=='unknown'
                ||data[i+a].nick_name=='null'||data[i+a].nick_name== undefined ){
                name=data[i+a].uid;
            }else {
                name=data[i+a].nick_name;
            };
            if(data[i+a].timestamp==''||data[i+a].timestamp=='unknown'
                ||data[i+a].timestamp=='null'||data[i+a].timestamp== undefined){
                time='暂无';
            }else {
                time=getLocalTime(data[i+a].timestamp);
            };
            if(data[i+a].photo_url==''||data[i+a].photo_url=='unknown'
                ||data[i+a].photo_url== undefined ||data[i+a].photo_url=='null'){
                photo='/static/images/unknown.png';
            }else {
                photo=data[i+a].photo_url;
            };
            if(data[i+a].text==''||data[i+a].text=='unknown'
                ||data[i+a].text=='null'||data[i+a].text== undefined){
                text='暂无';
            }else {
                text=data[i+a].text;
            };
            if(data[i+a].keywords_string==''||data[i+a].keywords_string=='unknown'
                ||data[i+a].keywords_string=='null'||data[i+a].keywords_string== undefined){
                key_words='暂无';
            }else {
                var word=data[i+a].keywords_string.split('&');
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
            oTBody.rows[i].insertCell(0);
            html_c =
                '<div class="weibo">'+
                '     <h3>'+
                '         <span id="mid" style="display: none">'+data[i+a].mid+'</span>'+
                '         <span>热点'+(i+a+1)+'：</span>'+
                '         <a href="###" class="user_name">'+name+'</a>&nbsp;'+
                '         <span>于</span>'+
                '         <b class="time">'+time+'</b>&nbsp;'+
                '         <span>发布</span>'+
                '     </h3>'+
                '     <div class="content">'+
                '         <div class="content-1">'+
                '               <img src="'+photo+'" alt="">'+
                '         </div>'+
                '         <div class="content-2">'+
                '               <span class="speech">'+ text+'</span>'+
                '               <p class="fd_nums">'+
                '                   <span>转发数:</span><b class="f_amount">'+data[i+a].retweeted+'</b>'+
                '                   <span>评论数:</span><b class="d_amount">'+data[i+a].comment+'</b>'+
                '               </p>'+
                '               <div class="content-3">'+
                '                   <span>关键词：</span>'+key_words+
                '                   <button class="judgment">热点研判</button>'+
                '               </div>'+
                '         </div>'+
                '     </div>'+
                ' </div>';
            oTBody.rows[i].cells[0].innerHTML = html_c;
            // $('.judgment').on('click',function () {
            //     var mid=$(this).parents('.weibo').find('#mid').text();
            //     window.open('/brust/result/?mid='+mid);
            // })
        }
    }

    $('.judgment').on('click',function () {
        var mid=$(this).parents('.weibo').find('#mid').text();
        window.open('/brust/result/?mid='+mid);
    })

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