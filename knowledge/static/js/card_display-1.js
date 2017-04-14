var cards_list =  result;
var name,photo,verified,location,tag,domain;
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
       location='未知';
    }else {
       location=data.location;
    };
    if (data.tag==''||data.tag=='unknown'||data.tag==0){
       tag='暂无';
    }else {
       var tag_1='';
       var words=data.tag;
       if (words.length<=3){
           tag_1=words.join(' ');
       }else {
           var key=words.splice(0,3).join(' ');
           var tit=words.splice(3).join(' ');
           tag_1+='<span title="'+tit+'">'+key+'</span> ';
       }
       tag=tag_1;
    };
    if (data.domain==''||data.domain=='unknown' ||data.domain=='null'){
       domain='未知';
    }else {
       domain=data.domain;
    };
    card+='<div class="per_card_details card" style="padding:10px 0 0 0;">'+
           '                <div class="details-1">'+
           '                    <div class="details-1-top">'+
           '                        <img src="'+photo+'" class="photo">'+
           '                        <img src="/static/images/per_xin.png" class="per_xin">'+
           '                        <p class="name" title="'+name+'">'+name+'</p>'+
           '                    </div>'+
           '                    <div class="details-1-bottom-left">'+
           '                        <p style="margin-top:12px;font-size: 8px"><b>认证类型：</b></p>'+
           '                        <p class="attest" title="'+verified+'">'+verified+'</p>'+
           '                        <img src="/static/images/position.png" title="位置"><span class="position">'+location+'</span>'+
           '                        <img src="/static/images/fansum.png" title="粉丝数"><span class="fansum">'+data.fansnum+'</span>'+
           '                    </div>'+
           '                    <div class="details-1-bottom-right">'+
           '                        <p style="margin-top:2px;font-size: 8px">'+
           '                            <b>业务标签：</b>'+
           '                            <span class="tag" title="'+tag+'">'+tag+'</span>'+
           '                        </p>'+
           '                        <p style="margin-top:2px;font-size: 8px">'+
           '                            <b>领域：</b>'+
           '                            <span class="field" title="'+domain+'">'+domain+'</span>'+
           '                        </p>'+
           '                        <p class="range" style="margin-top: 5px">'+
           '                            <img src="/static/images/influe.png" title="影响力"><span class="influe">'+data.influence.toFixed(2)+'</span>'+
           '                            <img src="/static/images/active.png" title="活跃度"><span class="active">'+data.activeness.toFixed(2)+'</span>'+
           '                            <img src="/static/images/sentive.png" title="敏感度"><span class="sentive">'+data.importance.toFixed(2)+'</span>'+
           '                        </p>'+
           '                    </div>'+
           '                </div>'+
           '            </div>';
}