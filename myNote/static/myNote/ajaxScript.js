var today = new Date();
var thisDay = today.getDate();
var thisYear = today.getFullYear();
var thisMonth = today.getMonth()+1;
const base_url = "http://ec2-54-238-57-49.ap-northeast-1.compute.amazonaws.com/";
const url1 = "ajax_view/";
const url2 = "schedule_view/";
const url3 = "sche_change/";
const url4 =  "sche_del/";

//ページ読み込み時の処理
$(function(){
    //カレンダー用Ajax通信
    $.ajax({
        url: base_url+url1,
        method: "GET",
        // プレーンテキストを受信（他にはhtml、xml、script、json、jsonp等）
        dataType: 'html',
        // リクエストパラメータ
        data: {
            year:thisYear,
            month:thisMonth,
        },
        timeout: 5000,
    })
    .done(function(data) {
        // 通信成功時の処理を記述
        $('#schedule_detail').html(data);
        $('.sche_titles ul li:first-child').click();
        if(thisMonth === 12){
            $('#premonth').attr({
                'value':thisMonth-1
            });
            $('#premonth').text(String(thisMonth-1)+"月");
            $('#nextmonth').attr({
                'value':1
            })
            $('#nextmonth').text("1月")
        }else if(thisMonth === 1){
            $('#premonth').attr({
                'value':12
            });
            $('#premonth').text("12月");
            $('#nextmonth').attr({
                'value':thisMonth+1
            })
            $('#nextmonth').text(String(thisMonth+1)+"月")
        }else{
            $('#premonth').attr({
                'value':thisMonth-1
            });
            $('#premonth').text(String(thisMonth-1)+"月");
            $('#nextmonth').attr({
                'value':thisMonth+1
            })
            $('#nextmonth').text(String(thisMonth+1)+"月")
        }
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('#schedule_detail').text('GET処理失敗.');
    });

    //予定追加用Ajax通信
    $.ajax({
        url: base_url+url2,
        method: "GET",
        // プレーンテキストを受信（他にはhtml、xml、script、json、jsonp等）
        dataType: 'html',
        // リクエストパラメータ
        data: {
            day:thisDay,
            year:thisYear,
            month:thisMonth,
        },
        timeout: 5000,
    })
    .done(function(data) {
        // 通信成功時の処理を記述
        $('#date_schedule').html(data);
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('#date_schedule').text('POST処理失敗.');
    });

    $('#alert_form').submit(function () { 
        if(window.confirm('本当に実行しますか？')){
            window.alert('変更を受け付けました。')
            return true;
        }
        else{
            window.alert('キャンセルしました。');
            return false;
        }
    });

    if(location.pathname === '/'){
        $('.todo').addClass('current_page');
    }else if(location.pathname === 'note/'){
        $('.mycode').addClass('current_page');
    }
})

//前の月のカレンダー取得
function preClick(){
    if(thisMonth === 1){
        thisYear -= 1;
        thisMonth = 12;
    }else{
        thisMonth -= 1;
    }
    $.ajax({
        url: base_url+url1,
        method: "GET",
        // プレーンテキストを受信（他にはhtml、xml、script、json、jsonp等）
        dataType: 'html',
        // リクエストパラメータ
        data: {
            year:thisYear,
            month:thisMonth,
        },
        timeout: 5000,
    })
    .done(function(data) {
        // 通信成功時の処理を記述
        $('#schedule_detail').html(data);
        if(thisMonth === 12){
            $('#premonth').attr({
                'value':thisMonth-1
            });
            $('#premonth').text(String(thisMonth-1)+"月");
            $('#nextmonth').attr({
                'value':1
            })
            $('#nextmonth').text("1月")
        }else if(thisMonth === 1){
            $('#premonth').attr({
                'value':12
            });
            $('#premonth').text("12月");
            $('#nextmonth').attr({
                'value':thisMonth+1
            })
            $('#nextmonth').text(String(thisMonth+1)+"月")
        }else{
            $('#premonth').attr({
                'value':thisMonth-1
            });
            $('#premonth').text(String(thisMonth-1)+"月");
            $('#nextmonth').attr({
                'value':thisMonth+1
            })
            $('#nextmonth').text(String(thisMonth+1)+"月")
        }
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('#schedule_detail').text('GET処理失敗.');
    });
}

//次の月のカレンダー取得
function nextClick(){
    if(thisMonth === 12){
        thisYear += 1;
        thisMonth = 1;
    }else{
        thisMonth += 1;
    }
    $.ajax({
        url: base_url+url1,
        method: "GET",
        // プレーンテキストを受信（他にはhtml、xml、script、json、jsonp等）
        dataType: 'html',
        // リクエストパラメータ
        data: {
            year:thisYear,
            month:thisMonth,
        },
        timeout: 5000,
    })
    .done(function(data) {
        // 通信成功時の処理を記述
        $('#schedule_detail').html(data);
        if(thisMonth === 12){
            $('#premonth').attr({
                'value':thisMonth-1
            });
            $('#premonth').text(String(thisMonth-1)+"月");
            $('#nextmonth').attr({
                'value':1
            })
            $('#nextmonth').text("1月")
        }else if(thisMonth === 1){
            $('#premonth').attr({
                'value':12
            });
            $('#premonth').text("12月");
            $('#nextmonth').attr({
                'value':thisMonth+1
            })
            $('#nextmonth').text(String(thisMonth+1)+"月")
        }else{
            $('#premonth').attr({
                'value':thisMonth-1
            });
            $('#premonth').text(String(thisMonth-1)+"月");
            $('#nextmonth').attr({
                'value':thisMonth+1
            })
            $('#nextmonth').text(String(thisMonth+1)+"月")
        }
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('#schedule_detail').text('GET処理失敗.');
    });
}

//カレンダー日付クリックイベント
function onclickTd(obj,year,month,date){
    $('td').removeClass('active');
    $(obj).addClass('active');
    $.ajax({
        url: base_url+url2,
        method: "GET",
        // プレーンテキストを受信（他にはhtml、xml、script、json、jsonp等）
        dataType: 'html',
        // リクエストパラメータ
        data: {
            day:date,
            year:year,
            month:month,
        },
        timeout: 5000,
    })
    .done(function(data) {
        // 通信成功時の処理を記述
        $('#date_schedule').html(data);
        $('.sche_titles ul li:first-child').click();
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('#date_schedule').text('POST処理失敗.');
    });
    month = String(month);
    date = String(date);
    if (month.length === 1){
        month = '0'+month;
    }
    if (date.length === 1){
        date = '0' +date;
    }
    let d = year + "-" + month + "-" + date;
    $('#id_date').attr({
        'value':d
    })
}

//スケジュール詳細クリックイベント
function sche_click(obj,num) {
    let a = `#sche_table table:nth-child(${num})`;
    $('#sche_table table').addClass('no_disp');
    $(a).removeClass('no_disp');
    $('.sche_titles ul li').removeClass('li_active');
    $(obj).addClass('li_active');
}

//スケジュール変更用　引数：スケジュールのID
function sche_change(id) {
    let my_id = id;
    $.ajax({
        url: base_url+url3,
        method: "GET",
        // プレーンテキストを受信（他にはhtml、xml、script、json、jsonp等）
        dataType: 'html',
        // リクエストパラメータ
        data: {
            id:my_id,
        },
        timeout: 5000,
    })
    .done(function(data) {
        // 通信成功時の処理を記述
        let my_url = url3+id+"/"
        $('.alert_cont form').attr('action', my_url)
        $('.alert h2').text("変更箇所を入力してください")
        $('.alert_cont form table').html(data);
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('.alert_cont').text('GET処理失敗.');
    });
    $('.alert').slideDown(1500);
}

//スケジュール削除用　引数：スケジュールのID
function sche_del(id) {
    let my_id = id;
    $.ajax({
        url: base_url+url4,
        method: "GET",
        // プレーンテキストを受信（他にはhtml、xml、script、json、jsonp等）
        dataType: 'html',
        // リクエストパラメータ
        data: {
            id:my_id,
        },
        timeout: 5000,
    })
    .done(function(data) {
        // 通信成功時の処理を記述
        let my_url = url4+id+"/"
        $('.alert_cont form').attr('action', my_url)
        $('.alert h2').text("この予定を本当に削除しますか？")
        $('.alert_cont form table').html(data);
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('.alert_cont').text('GET処理失敗.');
    });
    $('.alert').slideDown(1500);
}

function cancel(){
    $('.alert').slideUp(1000);
}