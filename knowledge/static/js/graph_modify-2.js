//关系选择
var start_type='User',end_type='User';
function one_type(value) {
    start_type=value;
    $('.manone').val('');
};
function two_type(value) {
    end_type=value;
    $('.mantwo').val('');
};

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
            if (start_type=='Event'){
                uid_1_name=item[1];
            }else {
                uid_2_name=item[1];
            }
        })
    }else {
        $.each(data_result,function (index,item) {
            if (item[1]==''||item[1]=='unknown'){
                data.push(item[0]+'<span class="_id" style="display:none;">'+item[0]+'</span>');
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
var uid_1,uid_2,uid_1_name,uid_2_name;

$(document).ready(function(){
    // $('.manone').attr('disabled',false);
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
                $('#container .rel_attributes .one .manone').blur();
            }else {
                if(jQuery.trim($('.append-2').html())==''){
                    return;
                }
                $('#container .rel_attributes .two .mantwo').blur();
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
            $('#container .rel_attributes .one .manone').blur();
        }else {
            $('#container .rel_attributes .two .mantwo').blur();
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
            $('#container .rel_attributes .one .manone').blur();
            var value = $('.addbg').text();
            uid_1=$('.addbg').children('._id').text();
            $('#container .rel_attributes .one .manone').val(value);
            $('.append-1').hide().html('');
            // $('.manone').attr('disabled',true);
        }else {
            $('#container .rel_attributes .two .mantwo').blur();
            var value = $('.addbg').text();
            uid_2=$('.addbg').children('._id').text();
            $('#container .rel_attributes .two .mantwo').val(value);
            $('.append-2').hide().html('');
            // $('.mantwo').attr('disabled',true);
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
        $('#container .rel_attributes .one .manone').val(value);
        $('.append-1').hide().html('');
        uid_1=$(obj).find('._id').text();
        uid_1_name=$(obj).find('._id').text();
        // $('.manone').attr('disabled',true);
    }else {
        $('#container .rel_attributes .two .mantwo').val(value);
        $('.append-2').hide().html('');
        uid_2=$(obj).find('._id').text();
        // $('.mantwo').attr('disabled',true);
    }

}

//---类似百度搜索功能----完---
var name_type_1,name_type_2,name_index_1,name_index_2;
$('#container .rel_submit').on('click',function () {
    if (one_value==''||two_value==''){
        alert('请输入节点。(不能为空)');
    }else {
        // var input_data=[];
        if (start_type=='User'){
            name_type_1='uid';
            name_index_1='node_index';
        }else if(start_type=='Org') {
            name_type_1='org_id';
            name_index_1='org_index';
        }else if(start_type=='Event') {
            name_type_1='event_id';
            name_index_1='event_index';
        }

        if (end_type=='User'){
            name_type_2='uid';
            name_index_2='node_index';
        } else if(end_type=='Org') {
            name_type_2='org_id';
            name_index_2='org_index';
        }else if(end_type=='Event') {
            name_type_2='event_id';
            name_index_2='event_index';
        }
        // input_data.push([
        //     name_type_1, uid_1, name_index_1,
        //     name_type_2, uid_2, name_index_2
        // ]);
        var input_url='/construction/relation_show_edit/?node_key1='+name_type_1+'&node1_id='+uid_1+
            '&node1_index_name='+name_index_1+'&node_key2='+name_type_2+'&node2_id='+uid_2+
            '&node2_index_name='+name_index_2;
        $.ajax({
            url: input_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:relation_add
        });
    }
})
var rel_table={
    "join":"参与事件",
    "discuss":"参与舆论",
    "other_relation":"其他关系",
    "contain":"主题关联",
    "event_other":"其他关系",
    "friend":"交互",
    "colleague":"业务关联",
    "organization_tag":"其他关系",
    "friend":"交互",
    "relative":"亲属",
    "leader":"上下级关系",
    "colleague":"自述关联",
    "ip_relation":"IP关联",
    "user_tag":"其他关系",
};
var rel_table_2={
    "参与事件":"join",
    "参与舆论":"discuss",
    "其他关系":"other_relation",
    "主题关联":"contain",
    "其他关系":"event_other",
    "交互":"friend",
    "业务关联":"colleague",
    "其他关系":"organization_tag",
    "亲属关系":"relative",
    "上下级关系":"leader",
    "自述关联":"colleague",
    "IP关联":"ip_relation",
    "其他关系":"user_tag",
};
function relation_add(data) {
    var data=eval(data);
    rel_list(data);
}
var _other;
function rel_list(data) {
    var show_rel=data[0].rel_list;
    var node1,node2;
    $('.relation .have').empty();
    if (data[0].node1[1]==''){
        node1 = data[0].node1[0];
    }else {
        node1 = data[0].node1[1];
    };
    if (data[0].node2[1]==''){
        node2 = data[0].node2[0];
    }else {
        node2 = data[0].node2[1];
    }
    //-------------
    $('#new_rel').empty();
    if (show_rel==''||show_rel=='NULL'||show_rel=='unknown'||show_rel.length==0){
        $('.relation .have').append('<span>暂无</span> ');
    }else {
        var tag='';
        for(var t=0;t<show_rel.length;t++){
            tag+=' <a>'+show_rel[t]+'</a> <b class="del icon icon-remove"></b>';
        }
        $('.relation .have').append(tag);
    };
    if ((((start_type=='User')||(start_type=='Org'))&&end_type=='Event')||
        (((end_type=='User')||(end_type=='Org'))&&start_type=='Event')){
        _other='other_relation';
        $('.relation #new_rel').append(
            '<option value="join" title="参与事件">参与事件</option>'+
            '<option value="discuss" title="参与舆论">参与舆论</option>'+
            '<option value="other_relation" title="其他关系">其他关系</option>'
        );
    }else if (start_type=='Event'&&end_type=='Event'){
        _other='event_other';
        $('.relation #new_rel').append(
            '<option value="contain" title="主题关联">主题关联</option>'+
            '<option value="event_other" title="其他关系">其他关系</option>'
        );
    }else if ((((start_type=='User')||(start_type=='Org'))&&end_type=='Org')||
        (((end_type=='User')||(end_type=='Org'))&&start_type=='Org')){
        _other='organization_tag';
        $('.relation #new_rel').append(
            '<option value="friend" title="交互">交互</option>'+
            '<option value="colleague" title="业务关联">业务关联</option>'+
            '<option value="organization_tag" title="其他关系">其他关系</option>'
        );
    } else if (start_type=='User'&&end_type=='User'){
        _other='user_tag';
        $('.relation #new_rel').append(
            '<option value="friend" title="交互">'+'交互'+'</option>'+
            '<option value="relative" title="亲属">亲属</option>'+
            '<option value="leader" title="上下级关系">上下级关系</option>'+
            '<option value="colleague" title="自述关联">自述关联</option>'+
            '<option value="ip_relation" title="IP关联">IP关联</option>'+
            '<option value="user_tag" title="其他关系">其他关系</option>'
        );
    }
    $('.relation').show();
    $('.del').on('click',function () {
        var pre=$(this).prev('a')[0].innerText;
        var delt_url;
        var reg=new RegExp("其他关系");
        if (reg.test(pre.toString())){
            delt_url='/construction/delete_relation/?node_key1='+name_type_1+'&node1_id='+uid_1+
                    '&node1_index_name='+name_index_1+'&node_key2='+name_type_2+'&node2_id='+uid_2+
                    '&node2_index_name='+name_index_2+'&rel='+_other+','+pre.toString().substr(5);
        }else {
            delt_url='/construction/delete_relation/?node_key1='+name_type_1+'&node1_id='+uid_1+
                '&node1_index_name='+name_index_1+'&node_key2='+name_type_2+'&node2_id='+uid_2+
                '&node2_index_name='+name_index_2+'&rel='+rel_table_2[pre];
        }
        $.ajax({
            url: delt_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:yes_no
        });
        $(this).prev().remove('a');
        $(this).remove();
    });
};
$('.yes').on('click',function () {
    var new_add=$('.relation #new_rel').val();
    var rel='';
    if (rel_table[new_add]=='其他关系'){
        var other=$('.other_rel').val();
        $('.relation .have').append(' <a title="'+new_add+'">其他关系-'+ other +'</a> <b class="del icon icon-remove"></b>');
        rel+=new_add+','+other;
    }else {
        if (new_add=='colleague'){
            if (start_type=='User'&&end_type=='User'){
                $('.relation .have').append(' <a>业务关联</a> <b class="del icon icon-remove"></b>');
            }else {
                $('.relation .have').append(' <a>自述关联</a> <b class="del icon icon-remove"></b>');
            }
        }else {
            $('.relation .have').append(' <a>'+ rel_table[new_add] +'</a> <b class="del icon icon-remove"></b>');
        }
        rel=new_add;
    };
    var creat_url='/construction/create_relation/?node_key1='+name_type_1+'&node1_id='+uid_1+
        '&node1_index_name='+name_index_1+'&node_key2='+name_type_2+'&node2_id='+uid_2+
        '&node2_index_name='+name_index_2+'&rel='+rel;
    $.ajax({
        url: creat_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:yes_no
    });
    $('.del').on('click',function () {
        var pre=$(this).prev('a')[0].innerText;
        var delt_url;
        var reg=new RegExp("其他关系");
        if (reg.test(pre.toString())){
            delt_url='/construction/delete_relation/?node_key1='+name_type_1+'&node1_id='+uid_1+
                '&node1_index_name='+name_index_1+'&node_key2='+name_type_2+'&node2_id='+uid_2+
                '&node2_index_name='+name_index_2+'&rel='+_other+','+pre.toString().substr(5);
        }else {
            delt_url='/construction/delete_relation/?node_key1='+name_type_1+'&node1_id='+uid_1+
                '&node1_index_name='+name_index_1+'&node_key2='+name_type_2+'&node2_id='+uid_2+
                '&node2_index_name='+name_index_2+'&rel='+rel_table_2[pre];
        }
        $.ajax({
            url: delt_url,
            type: 'GET',
            dataType: 'json',
            async: true,
            success:yes_no
        });
        $(this).prev().remove('a');
        $(this).remove();
    });
})
function add_rel(value) {
    if (value=='user_tag'||value=='organization_tag'||
        value=='event_other'||value=='other_relation'){
        $('.other_rel').show();
    }else {
        $('.other_rel').hide();
    }
};
function yes_no(data) {
    if (data== 1){
        alert('修改成功');
    }else {
        alert('修改失败');
    };
}

