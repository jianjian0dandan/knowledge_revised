//lcr 0424

function exportTableToCSV(filename)  
{
    // console.log('exportTableToCSV');
    person_data=result_1;

    var str =   "事件名称,"+$(".event_name").text()+"\n"+
                "实际发生地,"+$(".area").text()+"\n"+
                "事件类型,"+$(".type").text()+"\n"+
                "自动标签,"+$(".auto_tag").text()+"\n"+
                "业务标签,"+$(".bus_tag").text()+"\n"+
                "事件发生时间,"+$(".happen_time").text()+"\n"+
                "实际参与人物,"+$(".join_user").text()+"\n"+
                "实际参与机构,"+$(".agency").text()+"\n"+
                "微博数量,"+$(".weibo").text()+"\n"+
                "参与讨论人数,"+$(".discuss").text()+"\n"+
                "关注周期,"+$(".timefrom").text()+','+$(".timeto").text()+"\n";

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
    // console.log('click');
    filename="profile_"+result_1.name+".csv";
    exportTableToCSV.apply(this, [filename]);
    alert("素材导出成功！");
});