$(function(){
    var width = $('#main .content').width()/4;
    $('.todos').css({
        'width':width,
        'height':width
    });
    
    var delay_time = 0
    for (let i=0;i < $('.todo_task').length;i++){
        $(`.todo_task:eq(${i})`).delay(delay_time).slideDown(700);
        delay_time += 200
    }
})