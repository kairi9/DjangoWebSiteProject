from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from myNote.models import CalendarToDo
from django.contrib.auth import authenticate
from .models import LineAccount


line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')

class LineBot():
    def __init__(self,event):
        self.replyToken = event["replyToken"]
        self.msg_type = event["type"]
        self.mode = event["mode"]
        self.timestamp = event["timestamp"]
        self.source = event["source"]

    def add_schedule(self):
        a = CalendarToDo()
        try:
            obj = LineAccount.objects.get(line_id=self.source["userId"])
        except LineAccount.DoesNotExist as e:
            return e
        