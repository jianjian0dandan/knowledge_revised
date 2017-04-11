//-------------事件------------
var recommend_style='recommend',tt=0;
function event_type_2(value) {
    if(value==2){
        $('.event .manual').show();
        $('.event .manual-1').show();
        $('.event .manual-2').hide();
        $('.event .manual-2-2').hide();
        recommend_style='submit';
        tt=1;
    }else if (value==3){
        $('.event .manual').hide();
        $('.event .manual-1').hide();
        $('.event .manual-2').show();
        $('.event .manual-2-2').show();
        recommend_style='upload';
        tt=1;
    }else {
        $('.event .manual').hide();
        $('.event .manual-1').hide();
        $('.event .manual-2').hide();
        $('.event .manual-2-2').hide();
        recommend_style='recommend';
    }
}
//-------------事件--------完----

function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().substr(0,10)
};
var timestamp = Date.parse(new Date()),
// var timestamp = 1479571200,
    mid,key_string,time;
function weibo_content() {
    function place() {
        //this.ajax_method='GET'; // body...
    }
    place.prototype= {
        call_request:function(url,callback) {
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'json',
                async: true,
                success:callback
            });
        },
    };
    function territory(data) {
        var data=eval(data);
        Draw_weibo_table(data);
    };
    var place=new place();
    function nums() {
        var url = '/brust/show_weibo_list/?ts='+timestamp;
        place.call_request(url,territory);
    }
    nums();
    function Draw_weibo_table(data){
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
                html_c = "<p style='width:840px;text-align: center'>用户未发布任何微博</p>";
                oTBody.innerHTML = html_c;
            }else{

                for(i=0;i<parseInt(PageNo.value);i++)
                {                                                          //循环打印数组值
                    oTBody.insertRow(i);
                    var name,photo,area,key_words,key='';
                    if (dataArray[i].nick_name==''||dataArray[i].nick_name=='unknown') {
                        name=dataArray[i].uid;
                    }else {
                        name=dataArray[i].nick_name;
                    };
                    if (dataArray[i].photo_url==''||dataArray[i].photo_url=='unknown') {
                        photo=dataArray[i].uid;
                    }else {
                        photo='/static/images/unknown.png';
                    };
                    if (dataArray[i].geo==''||dataArray[i].geo=='unknown') {
                        area='未知';
                    }else {
                        area=dataArray[i].geo.replace(/&/g,' ');
                    };
                    key_words=dataArray[i].keywords_string.split('&').slice(0,5);
                    for (var kw=0;kw<key_words.length;kw++){
                        key+='<a>'+key_words[kw]+'</a>';
                    }
                    html_c =
                        '<div class="user">'+
                        '   <div class="user_left">'+
                        '       <img src="'+photo+'" alt="">'+
                        '   </div>'+
                        '   <div class="user_right">'+
                        '       <span id="mid" style="display:none;">'+dataArray[i].mid+'</span>'+
                        '       <span id="key_words" style="display:none;">'+dataArray[i].keywords_string+'</span>'+
                        '       <span id="timestamp" style="display:none;">'+dataArray[i].timestamp+'</span>'+
                        '       <a href="###" class="user_name">'+name+'</a>'+
                        '       <span><'+area+'></span>'+
                        '       <b class="time">'+getLocalTime(dataArray[i].timestamp)+'</b>&nbsp;<span>发表：</span>'+
                        '       <span class="speech">'+dataArray[i].text+'</span>'+
                        '       <div class="fd_nums">'+
                        '           <p style="float: left;">'+
                        '               <span>关键词：</span>'+key+
                        '               <button class="join_graph">加入图谱</button>'+
                        '           </p>'+
                        '           <span>转发数:</span><b class="f_amount">'+dataArray[i].retweeted+'</b>'+
                        '           <span>评论数:</span><b class="d_amount">'+dataArray[i].comment+'</b>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    oTBody.rows[i].insertCell(0);
                    oTBody.rows[i].cells[0].innerHTML = html_c;
                }
                $('#container #event_list .weibo_content .user .join_graph').on('click',function () {
                    mid=$(this).parents('.user').find('#mid').text();
                    key_string=$(this).parents('.user').find('#key_words').text();
                    time=$(this).parents('.user').find('#timestamp').text();
                    $('#relation_event .rel_list_event').empty();
                    $('#relation_event .rel_list_event').append(
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="contain" checked> 主题关联'+
                        '</label>'+
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="discuss" checked> 参与讨论'+
                        '</label>'+
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="join" checked> 参与事件'+
                        '</label>'
                    );
                    $('#relation_event').modal('show');
                });
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
                        var name,photo,area,key_words,key='';
                        if (dataArray[i].nick_name==''||dataArray[i].nick_name=='unknown') {
                            name=dataArray[i].uid;
                        }else {
                            name=dataArray[i].nick_name;
                        };
                        if (dataArray[i].photo_url==''||dataArray[i].photo_url=='unknown') {
                            photo=dataArray[i].uid;
                        }else {
                            photo='/static/images/unknown.png';
                        };
                        if (dataArray[i].geo==''||dataArray[i].geo=='unknown') {
                            area='未知';
                        }else {
                            area=dataArray[i].geo.replace(/&/g,' ');
                        };
                        key_words=dataArray[i].keywords_string.split('&').slice(0,5);
                        for (var kw=0;kw<key_words.length;kw++){
                            key+='<a>'+key_words[kw]+'</a>';
                        }
                        html_c =
                            '<div class="user">'+
                            '   <div class="user_left">'+
                            '       <img src="'+photo+'" alt="">'+
                            '   </div>'+
                            '   <div class="user_right">'+
                            '       <span id="mid" style="display:none;">'+dataArray[i].mid+'</span>'+
                            '       <span id="key_words" style="display:none;">'+dataArray[i].keywords_string+'</span>'+
                            '       <span id="timestamp" style="display:none;">'+dataArray[i].timestamp+'</span>'+
                            '       <a href="###" class="user_name">'+name+'</a>'+
                            '       <span><'+area+'></span>'+
                            '       <b class="time">'+getLocalTime(dataArray[i].timestamp)+'</b>&nbsp;<span>发表：</span>'+
                            '       <span class="speech">'+dataArray[i].text+'</span>'+
                            '       <div class="fd_nums">'+
                            '           <p style="float: left;">'+
                            '               <span>关键词：</span>'+key+
                            '               <button class="join_graph">加入图谱</button>'+
                            '           </p>'+
                            '           <span>转发数:</span><b class="f_amount">'+dataArray[i].retweeted+'</b>'+
                            '           <span>评论数:</span><b class="d_amount">'+dataArray[i].comment+'</b>'+
                            '       </div>'+
                            '   </div>'+
                            '</div>';
                        oTBody.rows[i].insertCell(0);
                        oTBody.rows[i].cells[0].innerHTML = html_c;
                    }
                    $('#container #event_list .weibo_content .user .join_graph').on('click',function () {
                        mid=$(this).parents('.user').find('#mid').text();
                        key_string=$(this).parents('.user').find('#key_words').text();
                        time=$(this).parents('.user').find('#timestamp').text();
                        $('#relation_event .rel_list_event').empty();
                        $('#relation_event .rel_list_event').append(
                            '<label class="checkbox-inline">'+
                            '   <input type="checkbox" value="contain" checked> 主题关联'+
                            '</label>'+
                            '<label class="checkbox-inline">'+
                            '   <input type="checkbox" value="discuss" checked> 参与讨论'+
                            '</label>'+
                            '<label class="checkbox-inline">'+
                            '   <input type="checkbox" value="join" checked> 参与事件'+
                            '</label>'
                        );
                        $('#relation_event').modal('show');
                    });
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
                    var name,photo,area,key_words,key='';
                    if (dataArray[i+a].nick_name==''||dataArray[i+a].nick_name=='unknown') {
                        name=dataArray[i+a].uid;
                    }else {
                        name=dataArray[i+a].nick_name;
                    };
                    if (dataArray[i+a].photo_url==''||dataArray[i+a].photo_url=='unknown') {
                        photo=dataArray[i+a].uid;
                    }else {
                        photo='/static/images/unknown.png';
                    };
                    if (dataArray[i+a].geo==''||dataArray[i+a].geo=='unknown') {
                        area='未知';
                    }else {
                        area=dataArray[i+a].geo.replace(/&/g,' ');
                    };
                    key_words=dataArray[i+a].keywords_string.split('&').slice(0,5);
                    for (var kw=0;kw<key_words.length;kw++){
                        key+='<a>'+key_words[kw]+'</a>';
                    }
                    oTBody.rows[i].insertCell(0);
                    html_c =
                        '<div class="user">'+
                        '   <div class="user_left">'+
                        '       <img src="'+photo+'" alt="">'+
                        '   </div>'+
                        '   <div class="user_right">'+
                        '       <span id="mid" style="display:none;">'+dataArray[i+a].mid+'</span>'+
                        '       <span id="key_words" style="display:none;">'+dataArray[i+a].keywords_string+'</span>'+
                        '       <span id="timestamp" style="display:none;">'+dataArray[i+a].timestamp+'</span>'+
                        '       <a href="###" class="user_name">'+name+'</a>'+
                        '       <span><'+area+'></span>'+
                        '       <b class="time">'+getLocalTime(dataArray[i+a].timestamp)+'</b>&nbsp;<span>发表：</span>'+
                        '       <span class="speech">'+dataArray[i+a].text+'</span>'+
                        '       <div class="fd_nums">'+
                        '           <p style="float: left;">'+
                        '               <span>关键词：</span>'+key+
                        '               <button class="join_graph">加入图谱</button>'+
                        '           </p>'+
                        '           <span>转发数:</span><b class="f_amount">'+dataArray[i+a].retweeted+'</b>'+
                        '           <span>评论数:</span><b class="d_amount">'+dataArray[i+a].comment+'</b>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    oTBody.rows[i].cells[0].innerHTML = html_c;
                    //数组从第i+a开始取值
                }
                $('#container #event_list .weibo_content .user .join_graph').on('click',function () {
                    mid=$(this).parents('.user').find('#mid').text();
                    key_string=$(this).parents('.user').find('#key_words').text();
                    time=$(this).parents('.user').find('#timestamp').text();
                    $('#relation_event .rel_list_event').empty();
                    $('#relation_event .rel_list_event').append(
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="contain" checked> 主题关联'+
                        '</label>'+
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="discuss" checked> 参与讨论'+
                        '</label>'+
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="join" checked> 参与事件'+
                        '</label>'
                    );
                    $('#relation_event').modal('show');
                });
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
                    var name,photo,area,key_words,key='';
                    if (dataArray[i+a].nick_name==''||dataArray[i+a].nick_name=='unknown') {
                        name=dataArray[i+a].uid;
                    }else {
                        name=dataArray[i+a].nick_name;
                    };
                    if (dataArray[i+a].photo_url==''||dataArray[i+a].photo_url=='unknown') {
                        photo=dataArray[i+a].uid;
                    }else {
                        photo='/static/images/unknown.png';
                    };
                    if (dataArray[i+a].geo==''||dataArray[i+a].geo=='unknown') {
                        area='未知';
                    }else {
                        area=dataArray[i+a].geo.replace(/&/g,' ');
                    };
                    key_words=dataArray[i+a].keywords_string.split('&').slice(0,5);
                    for (var kw=0;kw<key_words.length;kw++){
                        key+='<a>'+key_words[kw]+'</a>';
                    }
                    oTBody.rows[i].insertCell(0);
                    html_c =
                        '<div class="user">'+
                        '   <div class="user_left">'+
                        '       <img src="'+photo+'" alt="">'+
                        '   </div>'+
                        '   <div class="user_right">'+
                        '       <span id="mid" style="display:none;">'+dataArray[i+a].mid+'</span>'+
                        '       <span id="key_words" style="display:none;">'+dataArray[i+a].keywords_string+'</span>'+
                        '       <span id="timestamp" style="display:none;">'+dataArray[i+a].timestamp+'</span>'+
                        '       <a href="###" class="user_name">'+name+'</a>'+
                        '       <span><'+area+'></span>'+
                        '       <b class="time">'+getLocalTime(dataArray[i+a].timestamp)+'</b>&nbsp;<span>发表：</span>'+
                        '       <span class="speech">'+dataArray[i+a].text+'</span>'+
                        '       <div class="fd_nums">'+
                        '           <p style="float: left;">'+
                        '               <span>关键词：</span>'+key+
                        '               <button class="join_graph">加入图谱</button>'+
                        '           </p>'+
                        '           <span>转发数:</span><b class="f_amount">'+dataArray[i+a].retweeted+'</b>'+
                        '           <span>评论数:</span><b class="d_amount">'+dataArray[i+a].comment+'</b>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    oTBody.rows[i].cells[0].innerHTML = html_c;
                }
                $('#container #event_list .weibo_content .user .join_graph').on('click',function () {
                    mid=$(this).parents('.user').find('#mid').text();
                    key_string=$(this).parents('.user').find('#key_words').text();
                    time=$(this).parents('.user').find('#timestamp').text();
                    $('#relation_event .rel_list_event').empty();
                    $('#relation_event .rel_list_event').append(
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="contain" checked> 主题关联'+
                        '</label>'+
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="discuss" checked> 参与讨论'+
                        '</label>'+
                        '<label class="checkbox-inline">'+
                        '   <input type="checkbox" value="join" checked> 参与事件'+
                        '</label>'
                    );
                    $('#relation_event').modal('show');
                });
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
                var name,photo,area,key_words,key='';
                if (dataArray[i+a].nick_name==''||dataArray[i+a].nick_name=='unknown') {
                    name=dataArray[i+a].uid;
                }else {
                    name=dataArray[i+a].nick_name;
                };
                if (dataArray[i+a].photo_url==''||dataArray[i+a].photo_url=='unknown') {
                    photo=dataArray[i+a].uid;
                }else {
                    photo='/static/images/unknown.png';
                };
                if (dataArray[i+a].geo==''||dataArray[i+a].geo=='unknown') {
                    area='未知';
                }else {
                    area=dataArray[i+a].geo.replace(/&/g,' ');
                };
                key_words=dataArray[i+a].keywords_string.split('&').slice(0,5);
                for (var kw=0;kw<key_words.length;kw++){
                    key+='<a>'+key_words[kw]+'</a>';
                }
                oTBody.rows[i].insertCell(0);
                html_c =
                    '<div class="user">'+
                    '   <div class="user_left">'+
                    '       <img src="'+photo+'" alt="">'+
                    '   </div>'+
                    '   <div class="user_right">'+
                    '       <span id="mid" style="display:none;">'+dataArray[i+a].mid+'</span>'+
                    '       <span id="key_words" style="display:none;">'+dataArray[i+a].keywords_string+'</span>'+
                    '       <span id="timestamp" style="display:none;">'+dataArray[i+a].timestamp+'</span>'+
                    '       <a href="###" class="user_name">'+name+'</a>'+
                    '       <span><'+area+'></span>'+
                    '       <b class="time">'+getLocalTime(dataArray[i+a].timestamp)+'</b>&nbsp;<span>发表：</span>'+
                    '       <span class="speech">'+dataArray[i+a].text+'</span>'+
                    '       <div class="fd_nums">'+
                    '           <p style="float: left;">'+
                    '               <span>关键词：</span>'+key+
                    '               <button class="join_graph">加入图谱</button>'+
                    '           </p>'+
                    '           <span>转发数:</span><b class="f_amount">'+dataArray[i+a].retweeted+'</b>'+
                    '           <span>评论数:</span><b class="d_amount">'+dataArray[i+a].comment+'</b>'+
                    '       </div>'+
                    '   </div>'+
                    '</div>';
                oTBody.rows[i].cells[0].innerHTML = html_c;
            }
            $('#container #event_list .weibo_content .user .join_graph').on('click',function () {
                mid=$(this).parents('.user').find('#mid').text();
                key_string=$(this).parents('.user').find('#key_words').text();
                time=$(this).parents('.user').find('#timestamp').text();
                $('#relation_event .rel_list_event').empty();
                $('#relation_event .rel_list_event').append(
                    '<label class="checkbox-inline">'+
                    '   <input type="checkbox" value="contain" checked> 主题关联'+
                    '</label>'+
                    '<label class="checkbox-inline">'+
                    '   <input type="checkbox" value="discuss" checked> 参与讨论'+
                    '</label>'+
                    '<label class="checkbox-inline">'+
                    '   <input type="checkbox" value="join" checked> 参与事件'+
                    '</label>'
                );
                $('#relation_event').modal('show');
            });
        }

    }
};
weibo_content();


function sure_task_event() {
    var submit_user=$('#name').text();
    // var submit_user='admin';
    var status,event_rel=[];
    if($('#box1_e').is(':checked')) { status=1; };
    if($('#box2_e').is(':checked')) { status=2; };
    $("#relation_event .rel_list_event input:checkbox:checked").each(function (index,item) {
        event_rel.push($(this).val());
    });
    var event_rel_list=event_rel.join('&');
    var input_data ;
    if (tt=1){
        if (recommend_style=='upload'){
            // input_data={
                // 'submit_ts': timestamp, 'immediate_compute':status,'event_type':event_type,
                // 'relation_compute': event_rel_list, 'upload_data':updata_file_event,
                // 'submit_user':submit_user, 'recommend_style':recommend_style, 'compute_status':0
            // };
            input_data={
                'submit_ts': timestamp, 'immediate_compute':status, 'relation_compute': event_rel_list,
                'upload_data':updata_file_event, 'submit_user':submit_user,'recommend_style':recommend_style, 'compute_status':0,
                'start_ts':Date.parse(new Date(start_2))/1000, 'end_ts':Date.parse(new Date(end_2))/1000,
            }
        }else {
            input_data = {
                'submit_ts':timestamp, 'name':eventName, 'relation_compute': event_rel_list,
                'immediate_compute':status, 'keywords':key_words, 'start_ts':Date.parse(new Date(start))/1000,
                'end_ts':Date.parse(new Date(end))/1000, 'event_type':event_type, 'recommend_style':recommend_style,
                'compute_status':0, 'submit_user':submit_user,'event_ts':Date.parse(new Date())/1000,
            };
        }
    }else {
        input_data = {
            'submit_ts':timestamp, 'relation_compute': event_rel_list,
            'immediate_compute':status, 'keywords':key_string,
            'recommend_style':recommend_style, 'compute_status':0,
            'submit_user':submit_user,'event_ts':Number(time)
        }
    }
    var join_url;
    if (recommend_style=='upload'){
        join_url = '/construction/submit_event_file/';
    }else {
        join_url = '/construction/submit_event/';
    }

    $.ajax({
        type:'POST',
        url: join_url,
        contentType:"application/json",
        data: JSON.stringify(input_data),
        dataType: "json",
        success: yes_no
    });

}
//创建成功与失败
function yes_no(data) {
    var data=eval(data);
    console.log(data)
    if (data==0){
        $('#fail_success #prompt').text('创建失败,该事件已经入库。');
    }else {
        $('#fail_success #prompt').text('创建成功');
    }
    $('#fail_success').modal('show');
    event_task_renew();
}

//-----事件---任务列表
function event_task_renew() {
    var task_url='/construction/show_event_task/';
    $.ajax({
        url: task_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:task_list
    });
    function task_list(data) {
        var data = eval(data);
        $('#event').bootstrapTable('load', data);
        $('#event').bootstrapTable({
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
                    title: "事件名称",//标题
                    field: "name",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return value.replace(/&/,' ');
                    },
                },
                {
                    title: "添加方式",//标题
                    field: "recommend_style",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                        // if (row[6]=="influence"){
                        //     return '影响力推荐';
                        // }else if(row[6]=="sensitive"){
                        //     return '敏感度推荐';
                        // }else if(row[6]=="upload"){
                        //     return '上传文件';
                        // }else if(row[6]=="write"){
                        //     return '手动输入';
                        // }else if(row[6]=="auto"){
                        //     return '关注用户推荐';
                        // }
                    // }
                },
                {
                    title: "添加人",//标题
                    field: "submit_user",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //
                    // },
                },
                {
                    title: "提交时间",//标题
                    field: "submit_ts",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return getLocalTime(value);
                    },
                },
                {
                    title: "任务状态",//标题
                    field: "compute_status",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (value==0){
                            return '未计算';
                        }else if (value < 0){
                            return '正在计算';
                        }else if (value==1){
                            if (row.end_ts > Date.parse(new Date())){
                                return '正在跟踪';
                            }else if (row.end_ts <= Date.parse(new Date())){
                                return '计算完成';
                            }
                        }

                    },
                },
                {
                    title: "立即更新",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<a>立即更新</a>';
                    },
                },

            ],
            // onClickRow: function (row, tr) {
            //     if ($(tr.context).index()==2) {
            //         del_eventuid=row[0];
            //         $('#del_ject').modal("show");
            //     }
            // }
        });
    };
}
event_task_renew();

//--事件---推荐事件
var event_type=$('#event_lx-1').val;
// function event_lx(value) {
//
// }
//----文件传输--
var updata_file_event;
function handleFileSelect_event(evt){
    var files = evt;
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var a = oFREvent.target.result;
            $.ajax({
                type:"POST",
                url:"/construction/read_file/",
                dataType: "json",
                async:false,
                data:{new_words:a},
                success: function(data){
                    if( data ){
                        updata_file=[];
                        var data=data;
                        updata_file_event=data;
                        window.setTimeout(function () {
                            alert('上传成功。');
                        },500);
                    }
                }
            });
        };
        reader.readAsText(f,'GB2312');
    }
};

var key_words,start,end,start_2,end_2;
var eventName;
$('.add_sure').on('click',function () {
    if (node_type == 'event') {
        if (tt==1){
            if (recommend_style=='submit'){
                eventName=$('.node .event .event_name').val();
                key_words=$('.node .attributes .event .event_key').val();
                if (eventName==''){
                    alert('请输入事件名称。(不能为空)');
                }else {
                    if (key_words==''){
                        alert('请输入关键词。(不能为空)');
                    }else {
                        start=$('.event .start').val();
                        end=$('.event .end').val();
                        if (start>end){
                            alert('请检查时间，开始时间不能大于结束时间');
                        }else {
                            $('#relation_event .rel_list_event').empty();
                            $('#relation_event .rel_list_event').append(
                                '<label class="checkbox-inline">'+
                                '   <input type="checkbox" value="contain" checked> 主题关联'+
                                '</label>'+
                                '<label class="checkbox-inline">'+
                                '   <input type="checkbox" value="discuss" checked> 参与讨论'+
                                '</label>'+
                                '<label class="checkbox-inline">'+
                                '   <input type="checkbox" value="join" checked> 参与事件'+
                                '</label>'
                            );
                            $('#relation_event').modal('show');
                        }
                    }
                }
            }else if(recommend_style=='upload'){
                eventName=$('.node .event .event_name-2').val();
                start_2=$('.start-2').val();
                end_2=$('.end-2').val();
                if (eventName==''){
                    alert('请输入事件名称。(不能为空)');
                }else {
                    if (start_2>end_2){
                        alert('请检查时间，开始时间不能大于结束时间');
                    }else {
                        $('#relation_event .rel_list_event').empty();
                        $('#relation_event .rel_list_event').append(
                            '<label class="checkbox-inline">'+
                            '   <input type="checkbox" value="contain" checked> 主题关联'+
                            '</label>'+
                            '<label class="checkbox-inline">'+
                            '   <input type="checkbox" value="discuss" checked> 参与讨论'+
                            '</label>'+
                            '<label class="checkbox-inline">'+
                            '   <input type="checkbox" value="join" checked> 参与事件'+
                            '</label>'
                        );
                        $('#relation_event').modal('show');
                    }

                }

            }

        }
    }
});