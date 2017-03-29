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
var ids=[],
// 属性搜索
//与或非
yhf,yhf_key,yhf_value;
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
var no_ids=1;
$.each($("#container .start .options input"),function (index,item) {
    $(item).on('click',function () {
        if ($(this).val()==1){
            // ids=$('.start .options-1-value').val().split(',');
            no_ids=1;
        }else if ($(this).val()==2){
            //上传文件
            alert('文件中的内容请用逗号隔开(英文)隔开');
            ids=files_data;
            no_ids=2;
        }else if ($(this).val()==3){
            // 属性搜索
            //与或非
            no_ids=3;
            yhf_value=$('.start .options-2_down').val();
        }
    })
});
//--------文件传输----函数--
var files_data;
function start_handleFileSelect(evt){
    var files = evt;
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var a = oFREvent.target.result;
            files_data=a.split(',');
            window.setTimeout(function () {
                alert('上传成功');
            },500);
        };
        reader.readAsText(f,'GB2312');
    }
};

// //开始节点数据整理
var starts_nodes=[];

//--------------====起始节点------完---------

// if (no_ids==1){
//     ids=$('.start .options-1-value').val().split(',');
// }
// if (end_ids==1){
//     end_ids=$('.end .options-1-value').val().split(',');
// }

//--------------====终止节点-------开始============
var end_type='User';
function end(value) {
    if (value==1){
        end_type='User';
        $('.end #e_tag').empty();
        $('.end #e_tag').append(
            '<option value="uname">微博昵称</option>'+
            '<option value="description">个人描述</option>'+
            '<option value="function_mark">业务标签</option>'+
            '<option value="keywords">关键词</option>'+
            '<option value="hashtag">微话题</option>'+
            '<option value="location">注册地</option>'
        );
    }else if (value==2){
        end_type='Org';
        $('.end #e_tag').empty();
        $('.end #e_tag').append(
            '<option value="uname">微博昵称</option>'+
            '<option value="description">个人描述</option>'+
            '<option value="function_mark">业务标签</option>'+
            '<option value="keywords">关键词</option>'+
            '<option value="hashtag">微话题</option>'+
            '<option value="location">注册地</option>'
        );
    }else if (value==3){
        end_type='Event';
        $('.end #e_tag').empty();
        $('.end #e_tag').append(
            '<option value="name">事件名称</option>'+
            '<option value="keywords">自动标签</option>'+
            '<option value="work_tag">业务标签</option> '
        );
    }else if (value==4){
        end_type='SpecialEvent';
        $('.end #e_tag').empty();
        $('.end #e_tag').append(
            '<option value="topic_name">专题名称</option>'+
            '<option value="k_label">自动标签</option>'+
            '<option value="label">业务标签</option>'+
            '<option value="event">专题事件</option>'
        );
    }else if (value==5){
        end_type='Group';
        $('.end #e_tag').empty();
        $('.end #e_tag').append(
            '<option value="group_name">群体名称</option>'+
            '<option value="k_label">自动标签</option>'+
            '<option value="label">业务标签</option>'+
            '<option value="event">群体</option>'
        );
    }
}
//终止节点选择的输入方式
var end_ids=[];
// 属性搜索
//与或非
var end_yhf,end_yhf_key,end_yhf_value;

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
var end_no_ids=1;
$.each($("#container .end .options-3 input"),function (index,item) {
    $(item).on('click',function () {
        if ($(this).val()==1){
            // end_ids=$('.end .options-1-value').val().split(',');
            end_no_ids=1;
        }else if ($(this).val()==2){
            alert('文件中的内容请用逗号隔开(英文)隔开');
            end_no_ids=2;
            end_ids=end_files_data;
        }else if ($(this).val()==3){
            end_no_ids=3;
            end_yhf_value=$('.end .options-3_down').val();
        }
    })
});

//文件传输
var end_files_data;
function end_handleFileSelect(evt){
    var files = evt;
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var a = oFREvent.target.result;
            end_files_data=a.split(',');
            window.setTimeout(function () {
                alert('上传成功');
            },500);
        };
        reader.readAsText(f,'GB2312');
    }
};

var end_nodes=[];

//--------------====终止节点================完-------


//----------关系添加----------

var relation=[];
if ($('.advan-2 .rel-1-value').val()==''){
    null;
}else {
    relation.push($('.advan-2 .rel-1-value').val());
}
function show_rel() {
    $('#relation #rel_value_list').empty();
    if ((((start_type=='User')||(start_type=='Org'))&&end_type=='Event')||
        (((end_type=='User')||(end_type=='Org'))&&start_type=='Event')){
        $('#relation #rel_value_list').append(
            '<input type="checkbox" name="rels" value="join" title="参与事件"/>参与事件'+
            '<input type="checkbox" name="rels" value="discuss" title="参与舆论"/>参与舆论'+
            '<input type="checkbox" name="rels" value="other_relation" title="其他关系"/>其他关系'
        );
    }else if (start_type=='Event'&&end_type=='Event'){
        $('#relation #rel_value_list').append(
            '<input type="checkbox" name="rels" value="contain" title="主题关联"/>主题关联'+
            '<input type="checkbox" name="rels" value="event_other" title="其他关系"/>其他关系'
        );
    }else if ((((start_type=='User')||(start_type=='Org'))&&end_type=='Org')||
        (((end_type=='User')||(end_type=='Org'))&&start_type=='Org')){
        $('#relation #rel_value_list').append(
            '<input type="checkbox" name="rels" value="friend" title="交互"/>交互'+
            '<input type="checkbox" name="rels" value="colleague" title="业务关联"/>业务关联'+
            '<input type="checkbox" name="rels" value="organization_tag" title="其他"/>其他'
        );
    } else if (start_type=='User'&&end_type=='User'){
        $('#relation #rel_value_list').append(
            '<input type="checkbox" name="rels" value="friend" title="交互"/>交互'+
            '<input type="checkbox" name="rels" value="relative" title="亲属"/>亲属'+
            '<input type="checkbox" name="rels" value="leader" title="上下级关系"/>上下级关系'+
            '<input type="checkbox" name="rels" value="colleague" title="自述关联"/>自述关联'+
            '<input type="checkbox" name="rels" value="ip_relation" title="IP关联"/>IP关联'+
            '<input type="checkbox" name="rels" value="user_tag" title="其他"/>其他'
        );
    }
}
function rel_value() {
    $("[name=rels]:checkbox:checked").each(function (index,item) {
        relation.push($(this).val());
    });
}
//----------关系添加-----完-----



//高级搜索开始
var input_data;
$('#sure_advan').on('click',function () {
    //开始节点数据整理
    if (no_ids==1||no_ids==2){
        if (no_ids==1){
            ids.push($('.start .options-1-value').val());
        }
        starts_nodes.push(
            {
                'node_type':start_type,
                'ids':ids,
            }
        )
    }else {
        starts_nodes.push(
            {
                'node_type':start_type,
                'conditions':{
                    yhf:[{'wildcard':{yhf_key:yhf_value}}],
                }
            }
        )
    }
    //结束节点数据整理
    if (end_no_ids==1||end_no_ids==2){
        if (end_no_ids==1){
            end_ids.push($('.end .options-1-value').val());
        }
        end_nodes.push(
            {
                'node_type':end_type,
                'ids':end_ids,
            }
        )
    }else {
        end_nodes.push(
            {
                'node_type':end_type,
                'conditions':{
                    end_yhf:[{'wildcard':{end_yhf_key:end_yhf_value}}],
                }
            }
        )
    }

    if (yhf_value==''||end_yhf_value){
        alert('请输入起始节点/终止节点中属性搜索中的值。(不能为空)');
    }else if ($('.start .options-1-value').val()==''||$('.end .options-1-value').val()==''){
        alert('请输入起始节点/终止节点的值。(不能为空)');
    }else if (no_ids==2||end_no_ids==2){
        console.log(ids)
        if (ids==''||end_ids==''){
            alert('您还没有上传文件。(不能为空)');
        }
    } else {
        //--------其他信息----
        var step=$('.advan-4 .other .jump').val();
        var limit=$('.advan-4 .other .datanums').val();
        var short_path='False';
        if ($("[name=short]:checkbox").prop("checked")=='true'){
            short_path='True';
        };
//--------其他信息----完
        if (short_path=='True'){
            //此处要对起始节点进行判断，只能输入一个节点
            if(!(ids.length==1&&end_ids.length==1)){
                alert('因为您选择的是最短路径，所以起始节点和终止节点每项只能一个具体的节点。');
            }
        }else {
            input_data={
                'start_nodes':starts_nodes,
                'end_nodes':end_nodes,
                'relation':relation,
                'step':step,
                'limit':limit,
                'submit_user':submit_user,
                'short_path':short_path,
            }
        }
        relation=[];
        console.log(input_data)

        // var advanced_search_url = '/relation/submit_task/';
        // $.ajax({
        //     type:'POST',
        //     url: advanced_search_url,
        //     contentType:"application/json",
        //     data: JSON.stringify(input_data),
        //     dataType: "json",
        //     success: advanced_search
        // });
    }
})

function advanced_search(data) {
    var data=eval(data);
    search_to_result(data);
}
advanced_search(2222);


// {
//     'node_type':start_type,
//     'ids':ids,
//     'conditions':{
//     yhf:[{'wildcard':{yhf_key:yhf_value}}],
// }
// }
