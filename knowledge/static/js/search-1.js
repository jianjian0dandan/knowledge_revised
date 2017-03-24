//开始节点类型
var start_type='User';
function start(value) {
    if (value==1){
        start_type='User';
        $('.start #s_tag').empty();
        $('.start #s_tag').append(
            '<option value="uname">微博昵称</option>'+
            '<option value="description">个人描述</option>'+
            '<option value="function_mark">业务标签</option>'+
            '<option value="keywords">关键词</option>'+
            '<option value="hashtag">微话题</option>'+
            '<option value="location">注册地</option>'
        );
    }else if (value==2){
        start_type='Org';
        $('.start #s_tag').empty();
        $('.start #s_tag').append(
            '<option value="uname">微博昵称</option>'+
            '<option value="description">个人描述</option>'+
            '<option value="function_mark">业务标签</option>'+
            '<option value="keywords">关键词</option>'+
            '<option value="hashtag">微话题</option>'+
            '<option value="location">注册地</option>'
        );
    }else if (value==3){
        start_type='Event';
        $('.start #s_tag').empty();
        $('.start #s_tag').append(
            '<option value="name">事件名称</option>'+
            '<option value="keywords">自动标签</option>'+
            '<option value="work_tag">业务标签</option> '
        );
    }else if (value==4){
        start_type='SpecialEvent';
        $('.start #s_tag').empty();
        $('.start #s_tag').append(
            '<option value="topic_name">专题名称</option>'+
            '<option value="k_label">自动标签</option>'+
            '<option value="label">业务标签</option>'+
            '<option value="event">专题事件</option>'
        );
    }else if (value==5){
        start_type='Group';
        $('.start #s_tag').empty();
        $('.start #s_tag').append(
            '<option value="group_name">群体名称</option>'+
            '<option value="k_label">自动标签</option>'+
            '<option value="label">业务标签</option>'+
            '<option value="event">群体</option>'
        );
    }
}
//开始节点选择的输入方式
var ids=[];
$.each($("#container .start .options input"),function (index,item) {
    $(item).on('click',function () {
        if ($(this).val()==1){
            ids.push($('.start .options-1-value').val());
        }else if ($(this).val()==2){

        }else if ($(this).val()==3){

        }
    })
});

// 属性搜索
//与或非
var yhf,yhf_key;
function s_yhf(value) {
    if (value=='y'){
        yhf='must';
    }else if(value=='h'){
        yhf='should';
    }else if (value=='f'){
        yhf='must_not';
    }
};
function tag_start(value) {
    yhf_key=value;
}
var yhf_value=$('.start .options-2_down').val();
//--------------====起始节点------完---------


//--------------====终止节点-------开始============
var end_type='User';
function end(value) {
    if (value==1){
        end_type='User';
        $('.end #s-3-type').empty();
        $('.end #s-3-type').append(
            '<option value="uname">微博昵称</option>'+
            '<option value="description">个人描述</option>'+
            '<option value="function_mark">业务标签</option>'+
            '<option value="keywords">关键词</option>'+
            '<option value="hashtag">微话题</option>'+
            '<option value="location">注册地</option>'
        );
    }else if (value==2){
        end_type='Org';
        $('.end #s-3-type').empty();
        $('.end #s-3-type').append(
            '<option value="uname">微博昵称</option>'+
            '<option value="description">个人描述</option>'+
            '<option value="function_mark">业务标签</option>'+
            '<option value="keywords">关键词</option>'+
            '<option value="hashtag">微话题</option>'+
            '<option value="location">注册地</option>'
        );
    }else if (value==3){
        end_type='Event';
        $('.end #s-3-type').empty();
        $('.end #s-3-type').append(
            '<option value="name">事件名称</option>'+
            '<option value="keywords">自动标签</option>'+
            '<option value="work_tag">业务标签</option> '
        );
    }else if (value==4){
        end_type='SpecialEvent';
        $('.end #s-3-type').empty();
        $('.end #s-3-type').append(
            '<option value="topic_name">专题名称</option>'+
            '<option value="k_label">自动标签</option>'+
            '<option value="label">业务标签</option>'+
            '<option value="event">专题事件</option>'
        );
    }else if (value==5){
        end_type='Group';
        $('.end #s-3-type').empty();
        $('.end #s-3-type').append(
            '<option value="group_name">群体名称</option>'+
            '<option value="k_label">自动标签</option>'+
            '<option value="label">业务标签</option>'+
            '<option value="event">群体</option>'
        );
    }
}
//终止节点选择的输入方式
var end_ids=[];
$.each($("#container .end .options-3 input"),function (index,item) {
    $(item).on('click',function () {
        if ($(this).val()==1){
            ids.push($('.end .options-1-value').val());
        }else if ($(this).val()==2){

        }else if ($(this).val()==3){

        }
    })
});

// 属性搜索
//与或非
var end_yhf,end_yhf_key;
function e_yhf(value) {
    if (value=='y'){
        end_yhf='must';
    }else if(value=='h'){
        end_yhf='should';
    }else if (value=='f'){
        end_yhf='must_not';
    }
};
function tag_end(value) {
    end_yhf_key=value;
}
var end_yhf_value=$('.end .options-3_down').val();
//--------------====终止节点================完-------



//----------关系添加----------
if ()
var relation=[];
relation.push($('.advan-2 .rel-1-value').val());
function rel_value() {
    if($("[name=items]:checkbox").prop("checked",true)){

    }
}
//----------关系添加-----完-----



//高级搜索开始
var input_data;
$('#sure_advan').on('click',function () {
    input_data={
        'start_nodes':[
            {
                'node_type':start_type,
                'ids':ids,
                'conditions':{
                    yhf:[{'wildcard':{yhf_key:yhf_value}}],
                }
            }
        ],
        'end_nodes':[
            {
                'node_type':start_type,
                'ids':ids,
                'conditions':{
                    yhf:[{'wildcard':{yhf_key:yhf_value}}],
                }
            }
        ],
        'relation':relation,

    }
})