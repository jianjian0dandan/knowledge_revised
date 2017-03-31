$('#container .new_property .pro_sure').on('click',function () {
    var name=$('#container .new_property .theme_name').val();
    var tag=$('#container .new_property .theme_tag').val();
    var key=$('#container .new_property .key_words').val();
    var search_url='/theme/search_related_event_item/?item='+key+'&submit_user='+submit_user;
    $.ajax({
        url: search_url,
        type: 'GET',
        dataType: 'json',
        async: true,
        success:search
    });
})
function search(data) {
    var data=eval(data);

}