$('.event_name').text(result_1.name);
$('.event_name').attr('title',result_1.name);
if (result_1.real_geo==''||result_1.real_geo=='unknown' ||result_1.real_geo=='NULL'){
    $('.area').text('未知');
}else {
    $('.area').text(result_1.real_geo);
};
if (result_1.real_time==''||result_1.real_time=='unknown' ||result_1.real_time=='NULL'){
    $('.happen_time').text('未知');
}else {
    $('.happen_time').text(result_1.real_time);
};
if (result_1.event_type==''||result_1.event_type=='unknown' ||result_1.event_type=='NULL'){
    $('.type').text('未知');
}else {
    $('.type').text(result_1.event_type);
};

if (result_1.real_person==''||result_1.real_person=='unknown' ||result_1.real_person=='NULL'){
    $('.join_user').text('未知');
}else {
    var words=result_1.real_person.split('&');
    if (words.length<=3){
        $('.join_user').text(words.join(','));
    }else {
        var key=words.splice(0,3).join(',');
        $('.join_user').attr('title',key);
        $('.join_user').text(key);
    }

};
if (result_1.keywords==''||result_1.keywords=='unknown' ||result_1.keywords=='NULL'){
    $('.auto_tag').text('暂无');
}else {
    var words=result_1.keywords.split('&');
    if (words.length<=3){
        $('.auto_tag').text(words.join(','));
    }else {
        var key=words.splice(0,3).join(',');
        $('.auto_tag').attr('title',key);
        $('.auto_tag').text(key);
    }
};

if (result_1.real_auth==''||result_1.real_auth=='unknown' ||result_1.real_auth=='NULL'){
    $('.agency').text('暂无');
}else {
    var words=result_1.real_auth.split('&');
    if (words.length<=3){
        $('.agency').text(words.join(','));
    }else {
        var key=words.splice(0,3).join(',');
        $('.agency').attr('title',key);
        $('.agency').text(key);
    }
};

if (result_1.work_tag==''||result_1.work_tag=='unknown' ||result_1.work_tag.length==0){
    $('.bus_tag').text('暂无');
}else {
    var words=result_1.work_tag;
    if (words.length<=3){
        $('.bus_tag').text(words.join(','));
    }else {
        var key=words.splice(0,3).join(',');
        $('.bus_tag').attr('title',key);
        $('.bus_tag').text(key);
    }
};

$('.weibo').text(result_1.weibo_counts);
$('.discuss').text(result_1.uid_counts);
if (result_1.start_ts==''||result_1.start_ts=='unknown' ||result_1.start_ts=='NULL'){
    $('.timefrom').text('暂无');
}else {
    $('.timefrom').text(getLocalTime(result_1.start_ts));
};
if (result_1.end_ts==''||result_1.end_ts=='unknown' ||result_1.end_ts=='NULL'){
    $('.timeto').text('暂无');
}else {
    $('.timeto').text(getLocalTime(result_1.end_ts));
};

//===========================
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月|\//g, "-").replace(/日|上午|下午/g, " ").substr(0,10);
}