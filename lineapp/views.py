from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View
import json
from .linebot import LineBot
from .models import LineAccount
from django.contrib.auth import views as auth_views
from accounts.forms import MyLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .linebot import push_message


#LINEアカウントとの連携用
class LineLoginView(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    def get(self,request,line_id):
        a = LineAccount(username=request.user,line_id=line_id)
        a.save()
        push_message(line_id,"ログインに成功しました！")
        return HttpResponse('success')

#LINEBot用
class LineView(View):
    def post(self,request):
        req = json.loads(request.body.decode('utf-8'))
        events = req['events']
        for event in events:
            line_bot = LineBot(event)
            if event["type"] == "message":
                message = event["message"]["text"]
                if message == "今日の予定！":
                    line_bot.send_carousel()
                elif message == "予定の追加！":
                    pass
                elif message == "予定の変更！":
                    pass
                else:
                    line_bot.message_event(message)
            elif  event["type"] == "follow":
                line_bot.follow_event()
            elif  event["type"] == "postback":
                line_bot.postback_event()
            else:
                pass
        return HttpResponse(status=200)