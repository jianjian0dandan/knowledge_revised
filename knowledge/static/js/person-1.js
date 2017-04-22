//认证类型
var attest_type={
    '0':'名人','1':'政府','2':'企业', '3':'媒体',
    '4':'校园','5':'网站','6':'应用', '7':'团体(机构)','8':'待审机构',
    '-1':'普通用户','200':'初级达人','220':'中高级达人','400':'已故V用户'
};
//姓名
var name;
if (result_1.uname==""||result_1.uname=='NUll'||result_1.uname=='unknown'){
    name=result_1.uid;
}else {
    name=result_1.uname
}
$('.user_name').text(name);
$('.user_name').attr('title',name);
//基本信息
$('.ID').text(result_1.uid);
$('.happen_time').text(result_1.uname);
if (result_1.photo_url==''||result_1.photo_url=='unknown'
    ||result_1.photo_url=='NULL'){
    $('.in_photo img').attr('src','/static/images/unknown.png');
}else {
    $('.in_photo img').attr('src',result_1.photo_url);
};
if (result_1.verify_type in attest_type){
    if (result_1.verify_type==0||result_1.verify_type==200
        ||result_1.verify_type==220||result_1.verify_type==400){
        $('.attest').text('否');
    }else {
        $('.attest').text('是');
    }
    $('.attest_type').text(attest_type[result_1.verify_type]);
}else {
    $('.attest').text('否');
    $('.attest_type').text('未知');
}
if (result_1.description==''||result_1.description=='unknown'
    ||result_1.description=='NULL'){
    $('.description').text('暂无数据');
}else {
    $('.description').attr('title',result_1.description);
    $('.description').text(result_1.description);
};
if (result_1.location==''||result_1.location=='unknown'
    ||result_1.location=='NULL'){
    $('.place').text('未知');
}else {
    $('.place').text(result_1.location);
};
if (result_1.domain==''||result_1.domain=='unknown'
    ||result_1.domain=='NULL'){
    $('.identity').text('未知');
}else {
    $('.identity').text(result_1.domain);
};
if (result_1.domain==''||result_1.domain=='unknown'
    ||result_1.domain=='NULL'){
    $('.identity').text('未知');
}else {
    $('.identity').text(result_1.domain);
}

if (result_1.function_mark==''||result_1.function_mark=='unknown'
    ||result_1.function_mark.length==0){
    $('.tag').append('暂无');
}else {
    var tag='';
    var words=result_1.function_mark;
    if (words.length<=7){
        tag=words.join(',');
    }else {
        var key=words.splice(0,7).join(',');
        var tit=words.splice(7).join(',');
        tag+='<p title="'+tit+'">'+key+'</p> ';
    }
    $('.tag').append(tag);
};

if (result_4.fansnum==''||result_4.fansnum=='unknown'
    ||result_4.fansnum=='NULL'){
    $('.fansnum').text('0');
}else {
    $('.fansnum').text(result_4.fansnum);
};

if (result_4.statusnum==''||result_4.statusnum=='unknown'
    ||result_4.statusnum=='NULL'){
    $('.focus').text('0');
}else {
    $('.focus').text(result_4.statusnum);
}

if (result_4.friendnum==''||result_4.friendnum=='unknown'
    ||result_4.friendnum=='NULL'){
    $('.weibonum').text('0');
}else {
    $('.weibonum').text(result_4.friendnum);
}

var link='http://weibo.com/u/'+result_1.uid;
$('.weibo_link a').attr('href',link);
$('.weibo_link a').text(link);

$('.influ-1 .active0').text(result_1.activeness.toFixed(2));
if (result_1.activeness <= 33&&result_1.activeness >= 0) {
    $('.influ-1 .level0').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'
    );
}else if (result_1.activeness <= 66 &&result_1.activeness > 33) {
    $('.influ-1 .level0').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'
    );
}else if(result_1.activeness <= 100&&result_1.activeness > 66) {
    $('.influ-1 .level0').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'
    );
};

$('.influ-1 .active1').text(result_1.influence.toFixed(2));
if (result_1.influence <= 33&&result_1.influence >= 0) {
    $('.influ-1 .level1').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'
    );
}else if (result_1.influence <= 66 &&result_1.influence > 33) {
    $('.influ-1 .level1').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'
    );
}else if(result_1.influence <= 100 &&result_1.influence > 66) {
    $('.influ-1 .level1').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'
    );
};

$('.influ-1 .active2').text(result_1.sensitive.toFixed(2));
if (result_1.sensitive <= 33&&result_1.sensitive >= 0) {
    $('.influ-1 .level2').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'
    );
}else if (result_1.sensitive <= 66 &&result_1.sensitive > 33) {
    $('.influ-1 .level2').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-1.png"/>'
    );
}else if(result_1.sensitive <= 100 &&result_1.sensitive > 66) {
    $('.influ-1 .level2').append(
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'+
        '<img src="/static/images/wuxing-2.png"/>'
    );
}

if (result_1.activity_geo==''||result_1.activity_geo=='unknown'
    ||result_1.activity_geo=='NULL'){
    $('.activity .position').text('未知');
}else {
    $('.activity .position').text(result_1.activity_geo.replace(/&/g,' '));
};

if (result_1.activity_ip==''||result_1.activity_ip=='unknown'
    ||result_1.activity_ip=='NULL'){
    $('.activity .IP').text('未知');
}else {
    $('.activity .IP').text(result_1.activity_ip);
};

if (result_1.submit_ts==''||result_1.submit_ts=='unknown'
    ||result_1.submit_ts=='NULL'){
    $('.activity .time').text('未知');
}else {
    $('.activity .time').text(getLocalTime(result_1.submit_ts));
};

if (result_1.topic_string==''||result_1.topic_string=='unknown'
    ||result_1.hashtag=='NULL'){
    $('#person_content #content_left .preference .talk .talk_name').append('暂无');
}else {
    var tag='';
    var words=result_1.topic_string.split('&');
    if (words.length<=5){
        tag=words.join(',');
    }else {
        var key=words.splice(0,5).join(',');
        var tit=words.splice(5).join(',');
        tag+='<span title="'+tit+'">'+key+'</span> ';
    }
    $('#person_content #content_left .preference .talk .talk_name').append(tag);
};
//社交信息
var retweet=result_3.retweet;
var retweet_1=[],retweet_2=[];
for (var r in retweet){
    if (retweet[r]==''||retweet[r]=='NULL'||retweet[r]=='unknown'){
        retweet_1.push('<a uid="'+r+'">'+r+'</a>&nbsp;');
        retweet_2.push(r);
    }else {
        retweet_1.push('<a uid="'+r+'">'+retweet[r]+'</a>&nbsp;');
        retweet_2.push(retweet[r]);
    };
};
$('#person_content #content_left .social .soc_one .user').attr('title',retweet_2.join(','));
$('#person_content #content_left .social .soc_one .user').html(retweet_1);
$('#one').on('click',function () {
    $('#link .tit_h4').empty().text('转发');
    $('#link #link_content').empty();
    if (retweet_1.length==0||retweet_2.length==0){
        $('#link #link_content').text('没有数据');
    }else {
        for (var w=0;w<retweet_1.length;w++){
            $('#link #link_content').append(retweet_1[w]);
        }
    }
    $('#link').modal('show');
    $('#link #link_content a').on('click',function () {
        window.open('/index/person/?user_id='+$(this).attr('uid'));
    });
})

var beretweet=result_3.beretweet;
var beretweet_1=[],beretweet_2=[];
for (var r in beretweet){
    if (beretweet[r]==''||beretweet[r]=='NULL'||beretweet[r]=='unknown'){
        beretweet_1.push('<a uid="'+r+'">'+r+'</a>&nbsp;');
        beretweet_2.push(r);
    }else {
        beretweet_1.push('<a uid="'+r+'">'+beretweet[r]+'</a>&nbsp;');
        beretweet_2.push(beretweet[r]);
    };
};
$('#person_content #content_left .social .soc_two .user').attr('title',beretweet_2.join(','));
$('#person_content #content_left .social .soc_two .user').html(beretweet_1);
$('#two').on('click',function () {
    $('#link .tit_h4').empty().text('转发');
    $('#link #link_content').empty();
    if (beretweet_1.length==0||beretweet_1.length==0){
        $('#link #link_content').text('没有数据');
    }else {
        for (var w=0;w<beretweet_1.length;w++){
            $('#link #link_content').append(beretweet_1[w]);
        }
    }
    $('#link').modal('show');
    $('#link #link_content a').on('click',function () {
        window.open('/index/person/?user_id='+$(this).attr('uid'));
    });
})

var comment=result_3.comment;
var comment_1=[];
var comment_2=[];
for (var r in comment){
    if (comment[r]==''||comment[r]=='NULL'||comment[r]=='unknown'){
        comment_1.push('<a uid="'+r+'">'+r+'</a>&nbsp;');
        comment_2.push(r);
    }else {
        comment_1.push('<a uid="'+r+'">'+comment[r]+'</a>&nbsp;');
        comment_2.push(comment[r]);
    };
};
$('#person_content #content_left .social .soc_three .user').attr('title',comment_2.join(','));
$('#person_content #content_left .social .soc_three .user').html(comment_1);
$('#three').on('click',function () {
    $('#link .tit_h4').empty().text('转发');
    $('#link #link_content').empty();
    if (comment_1.length==0||comment_1.length==0){
        $('#link #link_content').text('没有数据');
    }else {
        for (var w=0;w<comment_1.length;w++){
            $('#link #link_content').append(comment_1[w]);
        }
    }
    $('#link').modal('show');
    $('#link #link_content a').on('click',function () {
        window.open('/index/person/?user_id='+$(this).attr('uid'));
    });
})

var becomment=result_3.becomment;
var becomment_1=[],becomment_2=[];
for (var r in becomment){
    if (becomment[r]==''||becomment[r]=='NULL'||becomment[r]=='unknown'){
        becomment_1.push('<a uid="'+r+'">'+r+'</a>&nbsp;');
        becomment_2.push(r);
    }else {
        becomment_1.push('<a uid="'+r+'">'+becomment[r]+'</a>&nbsp;');
        becomment_2.push(becomment[r]);
    };
};
$('#person_content #content_left .social .soc_four .user').attr('title',becomment_2.join(','));
$('#person_content #content_left .social .soc_four .user').html(becomment_1);
$('#four').on('click',function () {
    $('#link .tit_h4').empty().text('转发');
    $('#link #link_content').empty();
    if (becomment_1.length==0||becomment_1.length==0){
        $('#link #link_content').text('没有数据');
    }else {
        for (var w=0;w<becomment_1.length;w++){
            $('#link #link_content').append(becomment_1[w]);
        }
    }
    $('#link').modal('show');
    $('#link #link_content a').on('click',function () {
        window.open('/index/person/?user_id='+$(this).attr('uid'));
    });
})

$('#person_content #content_left .social .user a').on('click',function () {
    window.open('/index/person/?user_id='+$(this).attr('uid'));
});

//文本信息
function weibo(){
    $('#group_emotion_loading').css('display', 'none');
    // $('#input-table').css('display', 'block');
    var dataArray = result_5;
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
                var text,time;
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
                    '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
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
                    var text,time;
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
                        '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
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
                var text,time;
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
                    '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
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
                var text,time;
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
                    '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
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
            var text,time;
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
                '        <span class="time3">发表于&nbsp;<b>'+time+'</b></span>'+
                '        <span style="display: inline-block;float:right;">'+
                '        <span class="time4">转发数（'+dataArray[i+a].retweeted+'）</span>|&nbsp;'+
                '        <span class="time5">评论数（'+dataArray[i+a].comment+'）</span></span>'+
                '     </p>'+
                '</div>';
            oTBody.rows[i].cells[0].innerHTML = html_c;
        }
    }

}
weibo();


//===========================
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月|\//g, "-").replace(/日|上午|下午/g, " ");
}