
var cards_list =  result;
if (flag==1){
    var card='';
    var name,photo,verified,place,tag,domain;
    for (var key in cards_list){
        var data=cards_list[key];
        if (data.name==''||data.name=='unknown' ||data.name=='null'){
            name=key;
        }else {
            name=data.name;
        };
        if (data.picture==''||data.picture=='unknown' ||data.picture=='null'){
            photo='/static/images/unknown.png';
        }else {
            photo=data.picture;
        };
        if (data.verified==''||data.verified=='unknown' ||data.verified=='null'){
            verified='未认证';
        }else {
            verified=data.verified;
        };
        if (data.location==''||data.location=='unknown' ||data.location=='null'){
            place='未知';
        }else {
            place=data.location;
        };
        if (data.tag==''||data.tag=='unknown'||data.tag.length==0){
            tag='<span class="tag">暂无</span>';
            tit='';
        }else {
            var tag='';
            var words=data.tag;
            for(var w=0;w<=3;w++){
                tag+='<span class="tag">'+words[w]+'</span>';
            }
            tit=words.join(',');
        };
        if (data.domain==''||data.domain=='unknown' ||data.domain=='null'){
            domain='未知';
        }else {
            domain=data.domain;
        };
        card+='<div class="per_card_details card" style="padding:10px 0 0 0;">'+
            '                <span id="mid" style="display: none;">'+key+'</span>'+
            '                <span id="label" style="display: none;">'+tit+'</span>'+
            '                <div class="details-1">'+
            '                    <div class="details-1-top">'+
            '                        <img src="'+photo+'" class="photo">'+
            '                        <img src="/static/images/per_xin.png" class="per_xin">'+
            '                        <p class="name" title="'+name+'">'+name+'</p>'+
            '                    </div>'+
            '                    <div class="details-1-bottom-left">'+
            '                        <p style="margin-top:12px;font-size: 8px"><b>认证类型：</b></p>'+
            '                        <p class="attest" title="'+verified+'">'+verified+'</p>'+
            '                        <img src="/static/images/position.png" title="位置"><span class="position">'+place+'</span>'+
            '                        <img src="/static/images/fansum.png" title="粉丝数"><span class="fansum">'+data.fansnum+'</span>'+
            '                    </div>'+
            '                    <div class="details-1-bottom-right">'+
            '                        <p class="tag" style="margin-top:2px;font-size: 8px">'+
            '                            <b>业务标签：</b>'+tag+
            '                        </p>'+
            '                        <p style="margin-top:2px;font-size: 8px">'+
            '                            <b>领域：</b>'+
            '                            <span class="field" title="'+domain+'">'+domain+'</span>'+
            '                        </p>'+
            '                        <p class="range" style="margin-top: 5px">'+
            '                            <img src="/static/images/influe.png" title="影响力"><span class="influe">'+data.influence.toFixed(2)+'</span>'+
            '                            <img src="/static/images/active.png" title="活跃度"><span class="active">'+data.activeness.toFixed(2)+'</span>'+
            '                            <img src="/static/images/sentive.png" title="敏感度"><span class="sentive">'+data.importance+'</span>'+
            '                        </p>'+
            '                    </div>'+
            '                </div>'+
            '            </div>';
        $('.tag').attr('title',tit);
    }
}else if(flag==2){
    var card='';
    var name,time,place,tag;
    for (var key in cards_list){
        var data=cards_list[key];
        if (data.name==''||data.name=='unknown' ||data.name=='null'){
            name=key;
        }else {
            name=data.name;
        };
        if (data.time_ts==''||data.time_ts=='unknown' ||data.time_ts=='null'){
            time='未知';
        }else {
            time=data.time_ts;
        };
        if (data.geo==''||data.geo=='unknown' ||data.geo=='null'){
            place='未知';
        }else {
            place=data.geo;
        };
        if (data.tag==''||data.tag=='unknown'||data.tag.length==0){
            tag='<span class="tag">暂无</span>';
            tit='';
        }else {
            var tag='';
            var words=data.tag;
            for(var w=0;w<=3;w++){
                tag+='<span class="tag">'+words[w]+'</span>';
            }
            tit=words.join(',');
        };
        card+='<div class="event_card_details card">'+
            '                <span id="mid" style="display: none;">'+key+'</span>'+
            '                <span id="label" style="display: none;">'+tit+'</span>'+
            '                <div class="details-left">'+
            '                    <h3 class="name" title="'+name+'">'+name+'</h3>'+
            '                    <p>发生时间：<b class="time">'+time+'</b></p>'+
            '                </div>'+
            '                <div class="details-right">'+
            '                    <div class="details-right-1">'+
            '                        <p>'+
            '                            <img src="/static/images/gov_wei.png" title="位置"> <span class="position">'+place+'</span>'+
            '                            <img src="/static/images/gov_circle.png" class="heart evt_xin">'+
            '                        </p>'+
            '                        <p>'+
            '                            <img src="/static/images/gov_weibo.png" title="微博数"> <span class="weibonum">1223</span>'+
            '                            <img src="/static/images/gov_people.png" title="参与人数"> <span class="join">17223</span>'+
            '                        </p>'+
            '                    </div>'+
            '                    <div class="details-right-2">'+
            '                        <p class="type_e" style="margin: 10px 0">'+
            '                            <span style="font-weight: 800;font-size: 10px">事件类型：</span>'+
            '                            <span class="type">大学生</span>'+
            '                        </p>'+
            '                        <p class="tag_e" style="margin: 10px 0">'+
            '                            <span style="font-weight: 800;font-size: 10px">业务标签：</span>'+tag+
            '                        </p>'+
            '                        <p class="legend">'+
            '                            悟空和唐僧一起上某卫视非诚勿扰,悟空上台,24盏灯全灭。'+
            '                            理由:1.没房没车只有一根破棍.'+
            '                            2.保镖职业危险.'+
            '                            3.动不动打妖精,对女生不温柔.'+
            '                            4.坐过牢,曾被压五指山下500年。'+
            '                            唐僧上台，哗!灯全亮。'+
            '                            理由:1.公务员；'+
            '                            2.皇上兄弟，后台最硬'+
            '                            3.精通梵文等外语'+
            '                            4.长得帅'+
            '                            5.最关键一点：有宝马！'+
            '                        </p>'+
            '                    </div>'+
            '                </div>'+
            '            </span>';
        $('.tag_e').attr('title',tit);
    }
}else if(flag==0){
    var card='';
    var name,photo,place,tag,tit;
    for (var key in cards_list){
        var data=cards_list[key];
        if (data.name==''||data.name=='unknown' ||data.name=='null'){
            name=key;
        }else {
            name=data.name;
        };
        if (data.picture==''||data.picture=='unknown' ||data.picture=='null'){
            photo='/static/images/unknown.png';
        }else {
            photo=data.picture;
        };
        // if (data.verified==''||data.verified=='unknown' ||data.verified=='null'){
        //     verified='未认证';
        // }else {
        //     verified=data.verified;
        // };
        if (data.location==''||data.location=='unknown' ||data.location=='null'){
            place='未知';
        }else {
            place=data.location;
        };
        if (data.tag==''||data.tag=='unknown'||data.tag.length==0){
            tag='<span class="tag">暂无</span>';
            tit='';
        }else {
            var tag='';
            var words=data.tag;
            for(var w=0;w<=3;w++){
                tag+='<span class="tag">'+words[w]+'</span>';
            }
            tit=words.join(',');
        };
        card+='<div class="gov_card_details card" style="padding:30px 0 0 30px">'+
            '                <span id="mid" style="display: none;">'+key+'</span>'+
            '                <span id="label" style="display: none;">'+tit+'</span>'+
            '                <div class="details-1">'+
            '                    <div class="details-1-left">'+
            '                        <h3 class="name" title="'+name+'">'+name+'</h3>'+
            '                        <p>发生时间：<b class="time">2016-9-12</b></p>'+
            '                    </div>'+
            '                    <div class="details-1-right">'+
            '                        <img src="'+photo+'">'+
            '                    </div>'+
            '                    <div class="details-1-bottom">'+
            '                        <img src="/static/images/gov_wei.png" title="位置"> <span class="position">'+place+'</span>'+
            '                        <img src="/static/images/gov_people.png" title="粉丝数"> <span class="join">'+data.fansnum+'</span>'+
            '                        <img src="/static/images/gov_circle.png" class="heart org_xin">'+
            '                    </div>'+
            '                </div>'+
            '                <div class="details-2">'+
            '                    <span class="business">业务标签：</span>'+tag+
            '                </div>'+
            '            </div>';
        $('.details-2').attr('title',tit);
    };

}
$('#card_set').append(card);


//----
var p=1;
$('.per_xin').on('click',function () {
    if (p==1){
        $(this).attr('src','/static/images/per_focus.png');
        p=2;
        var uid=$(this).parents('.per_card_details').find('#mid').text();
        var user_name=$(this).parents('.per_card_details').find('.name').text();
        var label=$(this).parents('.per_card_details').find('#label').text();
        var data={'user_name':user_name,'uid':uid,'label':label};
        join_del.call_request(data,'/sysadmin/add_people/',yes_no);
    }else {
        $(this).attr('src','/static/images/per_xin.png');
        var user_name=$(this).parents('.per_card_details').find('.name').text();
        var data={'people_id':user_name};
        join_del.call_request(data,'/sysadmin/delete_focus_people/',yes_no);
        p=1;
    }
});
//-----------
var g=1;
$('.org_xin').on('click',function () {
    if (g==1){
        $(this).attr('src','/static/images/gov_xin.png');
        g=2;
        //-----
        var uid=$(this).parents('.gov_card_details').find('#mid').text();
        var user_name=$(this).parents('.gov_card_details').find('.name').text();
        var label=$(this).parents('.gov_card_details').find('#label').text();
        var data={'user_name':user_name,'uid':uid,'label':label};
        join_del.call_request(data,'/sysadmin/add_org/',yes_no);
        //------

    }else {
        $(this).attr('src','/static/images/gov_circle.png');
        var user_name=$(this).parents('.gov_card_details').find('.name').text();
        var data={'org_id':user_name};
        join_del.call_request(data,'/sysadmin/delete_focus_org/',yes_no);
        g=1;
    }
});
//------
var h=1;
$('.evt_xin').on('click',function () {
    if (h==1){
        $(this).attr('src','/static/images/gov_xin.png');
        //-----
        var uid=$(this).parents('.event_card_details').find('#mid').text();
        var user_name=$(this).parents('.event_card_details').find('.name').text();
        var label=$(this).parents('.event_card_details').find('#label').text();
        var data={'user_name':user_name,'uid':uid,'label':label};
        join_del.call_request(data,'/sysadmin/add_event/',yes_no);
        //------
        h=2;
    }else {
        $(this).attr('src','/static/images/gov_circle.png');
        var user_name=$(this).parents('.gov_card_details').find('.name').text();
        var data={'event_id':user_name};
        join_del.call_request(data,'/sysadmin/delete_focus_event/',yes_no);
        h=1;
    }
});

//--关注成功
function join_del(){};
join_del.prototype= {
    call_request:function(focus,url,callback) {
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            async: false,
            data:focus,
            success:callback
        });
    },
};
var join_del=new join_del();
function yes_no(data) {
    if(data=='Success'){
        alert('加入关注');
    }else if (data== 'Exist'){
        alert('已经在关注中');
    }else if(data=='success'){
        alert('取消关注');
    }
};
//-----

