//关系选择
var start_type='User',end_type='User',rel_type='friend';
function one_type(value) {
    start_type=value;
    rel();
};
function two_type(value) {
    end_type=value;
    rel();
};
var other;
function three_type(value) {
    if (value=='other_relation'||value=='event_other'
        ||value=='organization_tag'||value=='user_tag'){
        $('.other_value').show();
        other=0;
        rel_type=value;
    }else {
        rel_type=value;
        $('.other_value').hide();
    }
};
function rel() {
    $('#three-type').empty();
    if ((((start_type=='User')||(start_type=='Org'))&&end_type=='Event')||
        (((end_type=='User')||(end_type=='Org'))&&start_type=='Event')){
        $('#three-type').append(
            '<option value="join">参与事件</option>'+
            '<option value="discuss">参与舆论</option>'+
            '<option value="other_relation">其他关系</option>'
        );
    }else if (start_type=='Event'&&end_type=='Event'){
        $('#three-type').append(
            '<option value="contain">主题关联</option>'+
            '<option value="event_other">其他关系</option>'
        );
    }else if ((((start_type=='User')||(start_type=='Org'))&&end_type=='Org')||
        (((end_type=='User')||(end_type=='Org'))&&start_type=='Org')){
        $('#three-type').append(
            '<option value="friend">交互</option>'+
            '<option value="colleague">业务关联</option>'+
            '<option value="organization_tag">其他关系</option>'
        );
    } else if (start_type=='User'&&end_type=='User'){
        $('#three-type').append(
            '<option value="friend">交互</option>'+
            '<option value="relative">亲属</option>'+
            '<option value="leader">上下级关系</option>'+
            '<option value="colleague">自述关联</option>'+
            '<option value="ip_relation">IP关联</option>'+
            '<option value="user_tag">其他关系</option>'
        );
    }
}
//类似百度搜索功能
var one_value='',two_value='',search_data_url;
$('.manone').bind('input propertychange', function() {
    one_value=$('.manone').val();
    search_data_url='/construction/search_node/?node_type='+start_type+'&item='+one_value;
    $.ajax({
        url: search_data_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:search_data
    });
});
$('.mantwo').bind('input propertychange', function() {
    two_value=$('.mantwo').val();
    search_data_url='/construction/search_node/?node_type='+end_type+'&item='+two_value;
    $.ajax({
        url: search_data_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:search_data
    });

});

var data = [];
function search_data(look) {
    var data_result=eval(look);
    if (start_type=='Event'||end_type=='Event'){
        $.each(data_result,function (index,item) {
            data.push(item[1]+'<span class="_id" style="display:none;">'+item[0]+'</span>');
        })
    }else {
        $.each(data_result,function (index,item) {
            if (item[1]==''||item[1]=='unknown'){
                data.push(item[0]);
            }else {
                data.push(item[1]+'('+item[0]+')'+'<span class="_id" style="display:none;">'+item[0]+'</span>');
            }
        })
    }
}

var in_class;
function class_name(input_class) {
    in_class=$(input_class).attr('class');
}
var uid_1,uid_2;

$(document).ready(function(){
    $('.manone').attr('disabled',false);
    $(document).keydown(function(e){
        e = e || window.event;
        var keycode = e.which ? e.which : e.keyCode;
        if(keycode == 38){
            if (in_class=='manone'){
                if(jQuery.trim($('.append-1').html())==''){
                    return;
                }
            }else {
                if(jQuery.trim($('.append-2').html())==''){
                    return;
                }
            }
            movePrev();
        }else if(keycode == 40){
            if (in_class=='manone'){
                if(jQuery.trim($('.append-1').html())==''){
                    return;
                }
                $('#container .relation .rel_manual .one .manone').blur();
            }else {
                if(jQuery.trim($('.append-2').html())==''){
                    return;
                }
                $('#container .relation .rel_manual .two .mantwo').blur();
            }
            if($('.item').hasClass('addbg')){
                moveNext();
            }else{
                $('.item').removeClass('addbg').eq(0).addClass('addbg');
            }
        }else if(keycode == 13){
            dojob();
        }
    });
    var movePrev = function(){
        if (in_class=='manone'){
            $('#container .relation .rel_manual .one .manone').blur();
        }else {
            $('#container .relation .rel_manual .two .mantwo').blur();
        }
        var index = $('.addbg').prevAll().length;
        if(index == 0){
            $('.item').removeClass('addbg').eq($('.item').length-1).addClass('addbg');
        }else{
            $('.item').removeClass('addbg').eq(index-1).addClass('addbg');
        }
    }
    var moveNext = function(){
        var index = $('.addbg').prevAll().length;
        if(index == $('.item').length-1){
            $('.item').removeClass('addbg').eq(0).addClass('addbg');
        }else{
            $('.item').removeClass('addbg').eq(index+1).addClass('addbg');
        }
    };
    var dojob = function(){
        if (in_class=='manone'){
            $('#container .relation .rel_manual .one .manone').blur();
            var value = $('.addbg').text();
            uid_1=$('.addbg').children('._id').text();
            $('#container .relation .rel_manual .one .manone').val(value);
            $('.append-1').hide().html('');
            $('.manone').attr('disabled',true);
        }else {
            $('#container .relation .rel_manual .two .mantwo').blur();
            var value = $('.addbg').text();
            uid_2=$('.addbg').children('._id').text();
            $('#container .relation .rel_manual .two .mantwo').val(value);
            $('.append-2').hide().html('');
            $('.mantwo').attr('disabled',true);
        }

    }
});
function getContent(obj){
    var kw = jQuery.trim($(obj).val());
    if(kw == ''){
        if (in_class=='manone'){
            $('.append-1').hide().html('');
        }else {
            $('.append-2').hide().html('');
        }
        return false;
    }
    var html = '';
    for (var i = 0; i < data.length; i++) {
        if (data[i].indexOf(kw) >= 0) {
            html = html + "<div class='item' onmouseenter='getFocus(this)' onClick='getCon(this);'>" + data[i] + "</div>"
        }
    }
    if(html != ''){
        if (in_class=='manone'){
            $('.append-1').show().html(html);
        }else {
            $('.append-2').show().html(html);
        }
    }else{
        if (in_class=='manone'){
            $('.append-1').hide().html('');
        }else {
            $('.append-2').hide().html('');
        }
    }
    data = [];
}
function getFocus(obj){
    $('.item').removeClass('addbg');
    $(obj).addClass('addbg');
}
function getCon(obj){
    var value = $(obj).text();
    if (in_class=='manone'){
        $('#container .relation .rel_manual .one .manone').val(value);
        $('.append-1').hide().html('');
        uid_1=$(obj).find('._id').text();
        $('.manone').attr('disabled',true);
    }else {
        $('#container .relation .rel_manual .two .mantwo').val(value);
        $('.append-2').hide().html('');
        uid_2=$(obj).find('._id').text();
        $('.mantwo').attr('disabled',true);
    }

}

//---类似百度搜索功能----完---

//关系文件上传

//------

if($('input.ma_up:checkbox').attr("checked")==true) {

}
$('#container .relation .upload-2').on('click',function () {
    var name_type_1,name_type_2,name_index_1,name_index_2;
    var input_data=[];
    if (start_type=='User'||end_type=='User'){
        name_type_1='uid';
        name_index_1='node_index';
        name_type_2='uid';
        name_index_2='node_index';
    }else if(start_type=='Org'||end_type=='Org') {
        name_type_1='org_id';
        name_index_1='org_index';
        name_type_2='org_id';
        name_index_2='org_index';
    }else if(start_type=='Event'||end_type=='Event') {
        name_type_1='event_id';
        name_index_1='event_index';
        name_type_2='event_id';
        name_index_2='event_index';
    }
    if (other==0){
        var other_value=$('.three .other_value').val();
        if (other_value==''){
            alert('请输入您想要添加的关系。(不能为空)');
        }else {
            rel_type+=','+other_value;
            input_data.push([
                name_type_1, uid_1, name_index_1,
                rel_type,
                name_type_2, uid_2, name_index_2
            ]);
        }
    }else {
        input_data.push([
            name_type_1, uid_1, name_index_1,
            rel_type,
            name_type_2, uid_2, name_index_2
        ]);
    }
    var input_url='/construction/relation_add/';
    $.ajax({
        type:'POST',
        url: input_url,
        contentType:"application/json",
        data: JSON.stringify(input_data),
        dataType: "json",
        success: relation_add
    });
    console.log(input_data)
})
function relation_add(data) {
    var data=eval(data);
    console.log(data)
    if (data[0]==true){
        alert('关系添加成功。');
    }else {
        alert('关系添加失败。');
    }
}


