﻿    var user_name = $('#name').text();
    $("#focus_people").on('click',function () {
        $.ajax({   
            type:"POST",  
            url:"/index/show_attention/",
            dataType: "json",
            async:false,
            data:{user_name : user_name,s_type : 'people'},
            success: function(data){
            		
                if(data) {
                		$("#my_focus").empty();
                    var html = "<div class='details-1' style='text-align: center;margin-top: 17px'><span>名称</span><span>业务标签</span><span>关注时间</span><span>查看详情</span></div>";
                    if(data.length > 0){
                        for(var i=0;i < data.length;i += 1){
                            user = data[i];
                            html += "<div class='details-2'><span>"+user['name']+"</span><span>"+user['label']+"</span><span>"+user['time']+"</span><a style='font-size: 8px;color: white;' href='/index/person/?user_id="+user['uid']+"' target='_blank'>查看详情</a></div>";                            
                        }
                    }
                    else{
                        html += "<div class='details-2'><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span></div>";
                    }
                    html += "<button class='focus_more'  id='focus_more'>+查看更多</button>"
                    
                    $("#my_focus").append(html);
                }
                else{
                		$("#my_focus").empty();
                    var html = "<div class='details-1' style='text-align: center;margin-top: 17px'><span>名称</span><span>业务标签</span><span>关注时间</span><span>查看详情</span></div>";
                    html += "<div class='details-2'><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span></div>";
                    html += "<button class='focus_more'>+查看更多</button>"

                    $("#my_focus").append(html);
                } 
            }              
        });
    });
    $("#focus_event").on('click',function () {
        $.ajax({   
            type:"POST",  
            url:"/index/show_attention/",
            dataType: "json",
            async:false,
            data:{user_name : user_name,s_type : 'event'},
            success: function(data){
            		console.log(data);
                if(data) {
                    $("#my_focus").empty();
                    var html = "<div class='details-1' style='text-align: center;margin-top: 17px'><span>名称</span><span>业务标签</span><span>关注时间</span><span>查看详情</span></div>";
                    if(data.length > 0){
                        for(var i=0;i < data.length;i += 1){
                            user = data[i];
                            html += "<div class='details-2'><span>"+user['name']+"</span><span>"+user['label']+"</span><span>"+user['time']+"</span><a style='font-size: 8px;color: white;' href='/index/event/?user_id="+user['uid']+"' target='_blank'>查看详情</a></div>";                            
                        }
                    }
                    else{
                        html += "<div class='details-2'><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span></div>";
                    }
                    html += "<button class='focus_more'>+查看更多</button>"

                    $("#my_focus").append(html);
                }
                else{
                		$("#my_focus").empty();
                    var html = "<div class='details-1' style='text-align: center;margin-top: 17px'><span>名称</span><span>业务标签</span><span>关注时间</span><span>查看详情</span></div>";
                    html += "<div class='details-2'><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span></div>";
                    html += "<button class='focus_more'>+查看更多</button>"

                    $("#my_focus").append(html);
                } 
            }              
        });
    });
    $("#focus_org").on('click',function () {
        $.ajax({   
            type:"POST",  
            url:"/index/show_attention/",
            dataType: "json",
            async:false,
            data:{user_name : user_name,s_type : 'org'},
            success: function(data){
                if(data) {
                		$("#my_focus").empty();
                    var html = "<div class='details-1' style='text-align: center;margin-top: 17px'><span>名称</span><span>业务标签</span><span>关注时间</span><span>查看详情</span></div>";
                    if(data.length > 0){
                        for(var i=0;i < data.length;i += 1){
                            user = data[i];
                            html += "<div class='details-2'><span>"+user['name']+"</span><span>"+user['label']+"</span><span>"+user['time']+"</span><a style='font-size: 8px;color: white;' href='/index/organization/?user_id="+user['uid']+"' target='_blank'>查看详情</a></div>";                            
                        }
                    }
                    else{
                        html += "<div class='details-2'><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span></div>";
                    }
                    html += "<button class='focus_more'>+查看更多</button>"

                    $("#my_focus").append(html);
                }
                else{
                		$("#my_focus").empty();
                    var html = "<div class='details-1' style='text-align: center;margin-top: 17px'><span>名称</span><span>业务标签</span><span>关注时间</span><span>查看详情</span></div>";
                    html += "<div class='details-2'><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span><span>暂无数据</span></div>";
                    html += "<button class='focus_more'>+查看更多</button>"

                    $("#my_focus").append(html);
                } 
            }              
        });
    });