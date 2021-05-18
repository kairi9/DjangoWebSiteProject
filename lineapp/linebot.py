from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,CarouselTemplate,CarouselColumn,MessageAction,PostbackAction
from linebot.exceptions import LineBotApiError
from myNote.models import CalendarToDo
from django.contrib.auth import authenticate
from .models import LineAccount
from datetime import date

BASE_URL = "http://127.0.0.1:8000/"
LINE_URL = "lineapp/login/"
LOGO_URL = "static/myNote/mynote_logo.jpg"
line_bot_api = LineBotApi('iAgGuMTLq1lnXg1jpTdbEIG/yKZV9bkCNEpWtYRjI0Ix+DVAcMmq/0+D+km53QPkB168PW1k5a/hhFILx2gOwHEvVsh7fxHdeg+VXvGpjaDSpHrSqvsqN5tWB+oQMbkYl0H8Uv5xsD9/w2OlxW7x+QdB04t89/1O/w1cDnyilFU=')

#プッシュメッセージ
def push_message(user_id,text):
    try:
        line_bot_api.push_message(user_id,TextSendMessage(text=text))
    except LineBotApiError as e:
        print(e)

#今日の予定所得 return dict
def get_todays_schedule(user,date):
    try:
        data = CalendarToDo.objects.filter(username=user,date=date)
        details = []
        for d in data:
            date_sche = {'title':d.title,'start_time':d.start_time,'end_time':d.end_time,'date':d.date,'done':d.done,'discription':d.discription,'id':d.id}
            details.append(date_sche)
        return details
    except ValueError:
        details = []
        return details

#LINE Botクラス
class LineBot():
    def __init__(self,event):
        self.msg_type = event["type"]
        self.replyToken = event["replyToken"] if self.msg_type == "follow" or self.msg_type == "message" or self.msg_type == "postback" else None
        self.mode = event["mode"]
        self.timestamp = event["timestamp"]
        self.userId = event["source"]["userId"]
        self.postback = event["postback"] if self.msg_type == "postback" else None

    #メッセージイベント用
    def message_event(self,text):
        try:
            line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
        except LineBotApiError as e:
            print(e)

    #フォローイベント用
    def follow_event(self):
        text = "フォローありがとうございます！\nサービスを利用するためには、\nURLからログインをお願いします！\n"
        text += BASE_URL+LINE_URL+self.userId+"/"
        try:
            line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
        except LineBotApiError as e:
            print(e)

    #今日の予定をカーソルアクションで取得
    def get_today_event_as_carousel(self):
        #LINEアカウントが連携確認とユーザー取得
        try:
            user = LineAccount.objects.get(line_id=self.userId)
            user = user.username
        except LineAccount.DoesNotExist:
            self.follow_event()
            return None
        today = date.today()
        events = get_todays_schedule(user,today)
        #今日の予定がない場合
        if len(events)==0:
            text = "今日の予定はありません"
            push_message(self.userId,text)
        #今日の予定がある場合、予定をカーソルアクションとして配列に入れる
        else:
            columns = []
            for obj in events:
                #時間フォーマット
                s_hour,s_minute = str(obj["start_time"].hour),str(obj["start_time"].minute)
                f_hour,f_minute = str(obj["end_time"].hour),str(obj["end_time"].minute)
                start_time,end_time = '{}:{}'.format(s_hour.zfill(2),s_minute.zfill(2)), '{}:{}'.format(s_hour.zfill(2),s_minute.zfill(2))

                text = "{}\n{}~{}\n{}".format(obj["title"],start_time,end_time,obj["discription"])
                columns.append(
                    CarouselColumn(
                        thumbnail_image_url=BASE_URL+LOGO_URL,
                        title=str(obj["date"]),
                        text=text,
                        actions=[
                            PostbackAction(
                                label='変更',
                                display_text='変更',
                                data="re"+" "+str(obj["id"])
                            ),
                            PostbackAction(
                                label='削除',
                                display_text='削除',
                                data="del"+" "+str(obj["id"])
                            ),
                        ]
                    )
                )
            #カーソルをリッチメッセージオブジェクトとして返す
            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(columns=columns)
            )
            return carousel_template_message

    #リッチメッセージを送信
    def send_carousel(self):
        event = self.get_today_event_as_carousel()
        if event is not None:
            line_bot_api.reply_message(self.replyToken,event)
        return

    #ポストバックイベント
    def postback_event(self):
        postback_data = self.postback["data"]
        action, sche_id = postback_data.split(" ")
        #予定変更処理
        if action == "re":
            pass
        #予定削除処理
        elif action == "del":
            try:
                obj = CalendarToDo.objects.get(id=int(sche_id))
                obj.delete()
                text = "この予定を削除しました。"
            except:
                text = "予定の削除に失敗しました。"
            try:
                line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
            except LineBotApiError as e:
                print(e)
        return

    #予定追加処理
    def add_schedule(self):
        a = CalendarToDo()
        try:
            obj = LineAccount.objects.get(line_id=self.source["userId"])
        except LineAccount.DoesNotExist as e:
            text = "このサービスを使用するには\nURLからログインをお願いします！"
            text += BASE_URL+LINE_URL+self.userId+"/"
            text += "\nアカウントをお持ちでない場合は、\nアカウントを作成した後にもう一度このURLをクリックしてください。"
            try:
                line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
            except LineBotApiError as e:
                print(e)
        