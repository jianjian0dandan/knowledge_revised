//lcr 0424

function exportTableToCSV(filename)  
{
    console.log('exportTableToCSV');
    person_data=result_1;
    var photo_url;

    if (result_1.photo_url==''||result_1.photo_url=='unknown'
        ||result_1.photo_url=='NULL'){
        photo_url = '/static/images/unknown.png';
    }else {
        photo_url = result_1.photo_url;
    };

    if (result_1.verify_type in attest_type){
        if (result_1.verify_type==-1||result_1.verify_type==200
            ||result_1.verify_type==220||result_1.verify_type==400){
            person_data.verify_type='否';
        }else {
            person_data.verify_type='是';
        }
        $('.attest_type').text(attest_type[result_1.verify_type]);
    }else {
        person_data.verify_type='否';
    };

    if (result_1.description==''||result_1.description=='unknown'
        ||result_1.description=='NULL'){
        person_data.description ='暂无数据';
    };

    if (result_1.location==''||result_1.location=='unknown'
        ||result_1.location=='NULL'){
        person_data.place='未知';
    };

    if (result_1.domain==''||result_1.domain=='unknown'
        ||result_1.domain=='NULL'){
        person_data.identity='未知';
    };

    var weibo_link = 'http://weibo.com/u/'+result_1.uid;

    var str =   "微博ID,"+person_data.uid+"\n"+
                "人物昵称,"+person_data.uname+"\n"+
                "是否认证,"+person_data.verify_type+"\n"+
                "个人描述,"+person_data.description+"\n"+
                "注册地,"+person_data.location+"\n"+
                "身份,"+person_data.domain+"\n"+
                "粉丝数,"+$(".fansnum").text()+"\n"+
                "关注数,"+$(".focus").text()+"\n"+
                "微博数,"+$(".weibonum").text()+"\n"+
                "微博链接,"+weibo_link+"\n"+
                "业务标签,"+$(".tag").text()+"\n"+
                "头像链接,"+photo_url+"\n"+"\n"+"\n"+ 
                "关联类型,"+"名称,"+"ID"+"\n";

    if (result_2.people.length==0){
        str +=  "关联人物,"+"无数据,"+"无数据"+"\n";
    }else {
        $.each(data.people,function (index,item) {
            if (index==0){
                str +=  "关联人物,"+item[1]+","+item[0]+"\n";
            }else{
                str +=  " ,"+item[1]+","+item[0]+"\n";
            }
        });
    }
    str += '\n';
    str += "关联类型,"+"名称,"+"ID"+"\n";
    if (result_2.event.length==0){
        str +=  "关联事件,"+"无数据,"+"无数据"+"\n";
    }else {
        $.each(data.event,function (index,item) {
            if (index==0){
                str +=  "关联事件,"+item[1]+","+item[0]+"\n";
            }else{
                str +=  " ,"+item[1]+","+item[0]+"\n";
            }
        });
    }
    str += '\n';
    str += "关联类型,"+"名称,"+"ID"+"\n";
    if (result_2.org.length==0){
        str +=  "关联机构,"+"无数据,"+"无数据"+"\n";
    }else {
        $.each(data.people,function (index,item) {
            if (index==0){
                str +=  "关联机构,"+item[1]+","+item[0]+"\n";
            }else{
                str +=  " ,"+item[1]+","+item[0]+"\n";
            }
        });
    }
    str += '\n';
    str += "关联类型,"+"名称,"+"链接"+"\n";
    if (result_2.wiki.length==0){
        str +=  "关联知识,"+"无数据,"+"无数据"+"\n";
    }else {
        $.each(data.wiki,function (index,item) {
            if (index==0){
                str +=  "关联知识,"+item[0]+","+item[1]+"\n";
            }else{
                str +=  " ,"+item[0]+","+item[1]+"\n";
            }
        });
    }
    str += '\n';
    str += "关联类型,"+"名称,"+"ID"+"\n";
    if (result_2.doc.length==0){
        str +=  "关联资源,"+"无数据,"+"无数据"+"\n";
    }else {
        $.each(data.doc,function (index,item) {
            if (index==0){
                str +=  "关联资源,"+item[1]+","+item[0]+"\n";
            }else{
                str +=  " ,"+item[1]+","+item[0]+"\n";
            }
        });
    }

    str =  encodeURIComponent(str);  
    csvData = "data:text/csv;charset=utf-8,\ufeff"+str;  
    $(this).attr({
        'download': filename,
        'href': csvData,
        'target': '_blank'
    });
}  

$("a[id='material_out']").on('click', function (event) {
    filename="profile_"+result_1.uid+".csv";
    exportTableToCSV.apply(this, [filename]);
    alert("素材导出成功！");
});