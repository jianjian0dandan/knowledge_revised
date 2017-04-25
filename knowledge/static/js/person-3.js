//------------右边栏---
var data=result_2;
function link_source(data) {
    //关联人物
    var user=[];
    if (data.people.length==0|| (data.people.length==1&&data.people[0]=='')){
        $('.link_user .users').append(
            '<a>无数据</a>'
        );
    }else {
        $.each(data.people,function (index,item) {
            if (index<=4){
                $('.link_user .users').append(
                    '<a title="'+item[1]+'"><b style="display: none;">'+item[0]+'</b>'+item[1]+'</a>'
                )
            }else {
                user.push(
                    '<a title="'+item[1]+'"><b style="display: none;">'+item[0]+'</b>'+item[1]+'</a>'
                )
            }
        });
        $('.link_user .users a').on('click',function () {
            window.open('/index/person/?user_id='+$(this).find('b').text());
        });
    }
    //关联事件
    var event=[];
    if (data.event.length==0|| (data.event.length==1&&data.event[0]=='')){
        $('.link_event .events').append(
            '<a>无数据</a>'
        )
    }else {
        $.each(data.event,function (index,item) {
            if (index<=4){
                $('.link_event .events').append(
                    '<a title="'+item[1]+'"><b style="display: none;">'+item[0]+'</b>'+item[1]+'</a>'
                )
            }else {
                event.push(
                    '<a title="'+item[1]+'"><b style="display: none;">'+item[0]+'</b>'+item[1]+'</a>'
                )
            }
        });
        $('.link_event .events a').on('click',function () {
            window.open('/index/event/?user_id='+$(this).find('b').text());
        })
    }

    //关联机构
    var org=[];
    if (data.org.length==0|| (data.org.length==1&&data.org[0]=='')){
        $('.link_agency .agencys').append(
            '<a>无数据</a>'
        )
    }else {
        $.each(data.org,function (index,item) {
            if (index<=4){
                $('.link_agency .agencys').append(
                    '<a title="'+item[1]+'"><b style="display: none;">'+item[0]+'</b>'+item[1]+'</a>'
                )
            }else {
                org.push(
                    '<a title="'+item[1]+'"><b style="display: none;">'+item[0]+'</b>'+item[1]+'</a>'
                )
            }
        });
        $('.link_agency .agencys a').on('click',function () {
            window.open('/index/organization/?user_id='+$(this).find('b').text());
        })
    }

    //关联知识
    var wiki=[];
    if (data.wiki.length==0|| (data.wiki.length==1&&data.wiki[0]=='')){
        $('.link_knowledge .knowledge').append(
            '<a>无数据</a>'
        )
    }else {
        $.each(data.wiki,function (index,item) {
            if (index<=4){
                $('.link_knowledge .knowledge').append(
                    // '<a title="'+item[0]+'" href="'+item[1]+'">'+item[0]+'</a>'
                    '<a title="'+item[0]+'" href="###">'+item[0]+'</a>'
                )
            }else {
                wiki.push(
                    // '<a title="'+item[0]+'" href="'+item[1]+'">'+item[0]+'</a>'
                    '<a title="'+item[0]+'" href="###">'+item[0]+'</a>'
                )
            }
        });
        $('.link_knowledge .knowledge a').on('click',function () {
            window.open('/construction/wiki/?_id='+$(this).text());
        })
    }

    //关联资源
    var file=[];
    if (data.doc.length==0|| (data.doc.length==1&&data.doc[0]=='')){
        $('.link_resources .resources').append(
            '<a>无数据</a>'
        )
    }else {
        $.each(data.doc,function (index,item) {
            if (index<=4){
                $('.link_resources .resources').append(
                    '<a title="'+item[0]+'" href="'+item[1]+'">'+item[0]+'</a>'
                )
            }else {
                file.push(
                    '<a title="'+item[0]+'" href="'+item[1]+'">'+item[0]+'</a>'
                )
            }
        });
    }

    //-------人物------
    $('#person_content #content_right .link_user .user_more').on('click',function () {
        // $('#link .tit_h4').empty().text('关联人物');
        // $('#link #link_content').empty();
        // if (user.length==0){
        //     $('#link #link_content').text('没有更多数据');
        // }else {
        //     for (var u=0;u<user.length;u++){
        //         $('#link #link_content').append(user[u]);
        //     }
        // }
        // $('#link').modal('show');
        window.open('/index/cards/?user_id='+user_id+'&node_type=1&card_type=1');
    });

    //------事件-----
    $('#person_content #content_right .link_event .event_more').on('click',function () {
        // $('#link .tit_h4').empty().text('关联事件');
        // $('#link #link_content').empty();
        // if (event.length==0){
        //     $('#link #link_content').text('没有更多数据');
        // }else {
        //     for (var e=0;e<event.length;e++){
        //         $('#link #link_content').append(event[e]);
        //     }
        // }
        // $('#link').modal('show');
        window.open('/index/cards/?user_id='+user_id+'&node_type=1&card_type=2');
    });

    //-----机构-----
    $('#person_content #content_right .link_agency .agency_more').on('click',function () {
        // $('#link .tit_h4').empty().text('关联机构');
        // $('#link #link_content').empty();
        // if (org.length==0){
        //     $('#link #link_content').text('没有更多数据');
        // }else {
        //     for (var g=0;g<org.length;g++){
        //         $('#link #link_content').append(org[g]);
        //     }
        // }
        // $('#link').modal('show');
        window.open('/index/cards/?user_id='+user_id+'&node_type=1&card_type=0');
    });

    //-----知识-----
    $('#person_content #content_right .link_knowledge .knowledge_more').on('click',function () {
        $('#link .tit_h4').empty().text('关联知识');
        $('#link #link_content').empty();
        if (wiki.length==0){
            $('#link #link_content').text('没有更多数据');
        }else {
            for (var w=0;w<wiki.length;w++){
                $('#link #link_content').append(wiki[w]);
            }
        }
        $('#link').modal('show');
        $('#link a').on('click',function () {
            window.open('/construction/wiki/?_id='+$(this).text());
        })
    });

    //-----资源-----
    $('#person_content #content_right .link_resources .resources_more').on('click',function () {
        $('#link .tit_h4').empty().text('关联资源');
        $('#link #link_content').empty();
        if (file.length==0){
            $('#link #link_content').text('没有更多数据');
        }else {
            for (var f=0;f<file.length;f++){
                $('#link #link_content').append(file[f]);
            }
        }
        $('#link').modal('show');
    });

}
link_source(data);

//加入关注

$('#focus').on('click',function () {
        $(this).attr('src','/static/images/gov_xin.png');
        //-----
        var uid=user_id;
        var user_name=$('#name').text();
        var label=$('.tag').text();
        var data={'user_name':user_name,'uid':uid,'label':label};
        join_del.call_request(data,'/sysadmin/add_people/',yes_no);
        //------
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
        alert('加入关注成功！');
    }else if (data== 'Exist'){
        alert('已经在我的关注中！');
    }else{
        alert('加入关注失败！');
    }
};
//-----