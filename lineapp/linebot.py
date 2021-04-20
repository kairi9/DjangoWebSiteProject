from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,CarouselTemplate,CarouselColumn,MessageAction,PostbackAction
from linebot.exceptions import LineBotApiError
from myNote.models import CalendarToDo
from django.contrib.auth import authenticate
from .models import LineAccount
from datetime import date


URL = "https://78f75099936e.ngrok.io/lineapp/login/"
line_bot_api = LineBotApi('iAgGuMTLq1lnXg1jpTdbEIG/yKZV9bkCNEpWtYRjI0Ix+DVAcMmq/0+D+km53QPkB168PW1k5a/hhFILx2gOwHEvVsh7fxHdeg+VXvGpjaDSpHrSqvsqN5tWB+oQMbkYl0H8Uv5xsD9/w2OlxW7x+QdB04t89/1O/w1cDnyilFU=')

def push_message(user_id,text):
    try:
        line_bot_api.push_message(user_id,TextSendMessage(text=text))
    except LineBotApiError as e:
        print(e)


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

class LineBot():
    def __init__(self,event):
        self.msg_type = event["type"]
        self.replyToken = event["replyToken"] if self.msg_type == "follow" or self.msg_type == "message" or self.msg_type == "postback" else None
        self.mode = event["mode"]
        self.timestamp = event["timestamp"]
        self.userId = event["source"]["userId"]
        self.postback = event["postback"] if self.msg_type == "postback" else None

    def message_event(self,text):
        try:
            line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
        except LineBotApiError as e:
            print(e)

    def follow_event(self):
        text = "フォローありがとうございます！\nサービスを利用するためには、\nURLからログインをお願いします！\n"
        text += URL+self.userId+"/"
        try:
            line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
        except LineBotApiError as e:
            print(e)

    def get_today_event_as_carousel(self):
        try:
            user = LineAccount.objects.get(line_id=self.userId)
        except LineAccount.DoesNotExist:
            self.follow_event()
            return None
        today = date.today()
        events = get_todays_schedule(user,today)
        if len(events)==0:
            text = "今日の予定はありません"
            push_message(self.userId,text)
        else:
            columns = []
            for event in events:
                #時間フォーマット
                s_hour,s_minute = str(event.start_time.hour),str(event.start_time.minute)
                f_hour,f_minute = str(event.end_time.hour),str(event.end_time.minute)
                start_time,end_time = '{}:{}'.format(s_hour.zfill(2),s_minute.zfill(2)), '{}:{}'.format(s_hour.zfill(2),s_minute.zfill(2))

                text = "{}\n{}~{}\n{}".format(event["title"],start_time,end_time,event["discription"])
                columns.append(
                    CarouselColumn(
                        title=event["date"],
                        text=text,
                        actions=[
                            PostbackAction(
                                label='re-schedule',
                                display_text='変更',
                                data=event["id"]
                            ),
                            PostbackAction(
                                label='del-schedule',
                                display_text='削除',
                                data=event["id"]
                            ),
                        ]
                    )
                )

            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(columns=columns)
            )
            return carousel_template_message

    def send_carousel(self):
        event = self.get_today_event_as_carousel()
        if event is not None:
            line_bot_api.reply_message(self.replyToken,event)
        return

    def postback_event(self):
        postback_data = self.postback["data"]
        
        return

    def add_schedule(self):
        a = CalendarToDo()
        try:
            obj = LineAccount.objects.get(line_id=self.source["userId"])
        except LineAccount.DoesNotExist as e:
            text = "このサービスを使用するには\nURLからログインをお願いします！"
            text += URL+self.userId+"/"
            text += "\nアカウントをお持ちでない場合は、\nアカウントを作成した後にもう一度このURLをクリックしてください。"
            try:
                line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
            except LineBotApiError as e:
                print(e)
        