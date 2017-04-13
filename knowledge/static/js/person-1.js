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

if (result_1.hashtag==''||result_1.hashtag=='unknown'
    ||result_1.hashtag=='NULL'){
    $('.tag').append('暂无');
}else {
    var tag='';
    var words=result_1.hashtag.split('&');
    if (words.length<=7){
        tag=words.join(',');
    }else {
        var key=words.splice(0,7).join(',');
        var tit=words.splice(7).join(',');
        tag+='<p title="'+tit+'">'+key+'</p> ';
    }
    $('.tag').append(tag);
};
$('.fansnum').text();
$('.focus').text();
$('.weibonum').text();
var link='http://weibo.com/u/'+result_1.uid;
$('.weibo_link a').attr('href',link);
$('.weibo_link a').text(link);

$('.influ-1 .active0').text(result_1.activeness.toFixed(2));
if (result_1.activeness <= 33&&result_1.activeness >= 0) {
    $('.influ-1 .level0').text('低');
}else if (result_1.activeness <= 66 &&result_1.activeness > 33) {
    $('.influ-1 .level0').text('中');
}else if(result_1.activeness <= 100&&result_1.activeness > 66) {
    $('.influ-1 .level0').text('高');
};

$('.influ-1 .active1').text(result_1.influence.toFixed(2));
if (result_1.influence <= 33&&result_1.influence >= 0) {
    $('.influ-1 .level1').text('低');
}else if (result_1.influence <= 66 &&result_1.influence > 33) {
    $('.influ-1 .level1').text('中');
}else if(result_1.influence <= 100 &&result_1.influence > 66) {
    $('.influ-1 .level1').text('高');
};

$('.influ-1 .active2').text(result_1.sensitive.toFixed(2));
if (result_1.sensitive <= 33&&result_1.sensitive >= 0) {
    $('.influ-1 .level2').text('低');
}else if (result_1.sensitive <= 66 &&result_1.sensitive > 33) {
    $('.influ-1 .level2').text('中');
}else if(result_1.sensitive <= 100 &&result_1.sensitive > 66) {
    $('.influ-1 .level2').text('高');
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

//===========================
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日|上午|下午/g, " ");
}