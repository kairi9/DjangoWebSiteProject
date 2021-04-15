from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from myNote.models import CalendarToDo
from django.contrib.auth import authenticate
from .models import LineAccount

URL = "https://273d2a7a9353.ngrok.io/lineapp/login/"
line_bot_api = LineBotApi('iAgGuMTLq1lnXg1jpTdbEIG/yKZV9bkCNEpWtYRjI0Ix+DVAcMmq/0+D+km53QPkB168PW1k5a/hhFILx2gOwHEvVsh7fxHdeg+VXvGpjaDSpHrSqvsqN5tWB+oQMbkYl0H8Uv5xsD9/w2OlxW7x+QdB04t89/1O/w1cDnyilFU=')

def push_message(user_id,text):
    try:
        line_bot_api.push_message(user_id,TextSendMessage(text=text))
    except LineBotApiError as e:
        print(e)

class LineBot():
    def __init__(self,event):
        self.replyToken = event["replyToken"]
        self.msg_type = event["type"]
        self.mode = event["mode"]
        self.timestamp = event["timestamp"]
        self.userId = event["source"]["userId"]

    def message_event(self,text):
        try:
            line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
        except LineBotApiError as e:
            print(e)

    def follow_event(self):
        text = "フォローありがとうございます！\nURLからログインをお願いします！\n"
        text += URL+self.userId+"/"
        try:
            line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
        except LineBotApiError as e:
            print(e)

    def postback_event(self):
        pass

    def add_schedule(self):
        a = CalendarToDo()
        try:
            obj = LineAccount.objects.get(line_id=self.source["userId"])
        except LineAccount.DoesNotExist as e:
            text = "このサービスを使用するには\nURLからログインをお願いします！\n"
            text += URL+self.userId+"/"
            try:
                line_bot_api.reply_message(self.replyToken,TextSendMessage(text=text))
            except LineBotApiError as e:
                print(e)
        