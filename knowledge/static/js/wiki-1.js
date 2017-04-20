var wiki_url='/construction/show_wiki/';
var input_data = {'name':'日常生活'};
$.ajax({
    url: wiki_url,
    type: 'POST',
    // dataType: 'string',
    contentType:"application/json",
    data: JSON.stringify(input_data),
    async: true,
    success:wiki_body
});
function wiki_body(data) {
    console.log(data)
    $('#content').html(data);
}


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
    $('.user_name').append(data['name']);
    $('#main').append(data['content']);
}
function wiki_related(data) {
     console.log(data);
    //关联人物
    var user=[];
    if (data['User'].length==0){
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
    if (data['Event'].length==0){
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
    if (data['Org'].length==0){
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
    }
}