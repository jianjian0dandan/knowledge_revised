var wiki_url='/construction/show_wiki/';
var input_data = {'name':user_id};
$.ajax({
    url: wiki_url,
    type: 'POST',
    // dataType: 'string',
    contentType:"application/json",
    data: JSON.stringify(input_data),
    async: true,
    success:wiki_body
});
var txt;
function wiki_body(data) {
    $('#content').html(data);
    $('#content a').on('click',function () {
        var _href=$(this).attr('href');
        $(this).attr('href','javascript:void(0);');
        if (_href.substr(0,5)=='/wiki'){
            txt=$(this).text();
            var wiki_exit_url = '/construction/wikinode_exist/';
            wiki.call_request(wiki_exit_url,wiki_exit);
        }else {
            alert('该词条暂未收录。');
        };
        if ($(this).text()=='编辑'){
            alert('暂时无法操作，给您带来不便，请谅解。')
        }
    });
    $('#content img').attr('src','/static/images/unknown.png');
}
function wiki_exit(data) {
    if (data=='1'){
        window.open('/construction/wiki/?_id='+txt);
    }else {
        alert('该词条暂未收录。');
    }
}

var _wiki_url;
function wiki() {};
wiki.prototype= {
    call_request:function(url,callback) {
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            contentType:"application/json",
            data: JSON.stringify(input_data),
            async: true,
            success:callback
        });
    },
};
var wiki=new wiki();
function nums() {
    var wiki_basic_url = '/construction/show_wiki_basic/';
    var wiki_related_url = '/construction/show_wiki_related/';
    wiki.call_request(wiki_basic_url,wiki_basic);
    wiki.call_request(wiki_related_url,wiki_related);
}
nums();
function wiki_basic(data) {
    console.log(data)
    _wiki_url=data.url;
    // $('.user_name').append(data['name']);
    $('#main').append(data['content']);
}
function wiki_related(data) {
    console.log(data);
    if (data==''){
        alert('该词条暂未收录,无法为您展示。');
    }
    //关联人物
    var user=[];
    if (data['User'].length==0||(data['User'].length==1&&data['User'][0]=='')){
        $('.link_user .users').append(
            '<a>无数据</a>'
        );
    }else {
        $.each(data['User'],function (index,item) {
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
    if (data['Event'].length==0||(data['Event'].length==1&&data['Event'][0]=='')){
        $('.link_event .events').append(
            '<a>无数据</a>'
        )
    }else {
        $.each(data['Event'],function (index,item) {
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
    if (data['Org'].length==0||(data['Org'].length==1&&data['Org'][0]=='')){
        $('.link_agency .agencys').append(
            '<a>无数据</a>'
        )
    }else {
        $.each(data['Org'],function (index,item) {
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
    };
    //-------人物------
    $('#container #content_right .link_user .user_more').on('click',function () {
        window.open('/index/cards/?user_id='+_wiki_url+'&node_type=5&card_type=1');
    });

    //------事件-----
    $('#container #content_right .link_event .event_more').on('click',function () {
        window.open('/index/cards/?user_id='+_wiki_url+'&node_type=5&card_type=2');
    });

    //-----机构-----
    $('#container #content_right .link_agency .agency_more').on('click',function () {
        window.open('/index/cards/?user_id='+_wiki_url+'&node_type=5&card_type=0');
    });
}

$('#chart').on('click',function () {
    window.open('/index/graph/?user_id='+_wiki_url+'&node_type=wiki');
});