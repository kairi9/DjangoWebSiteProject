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


# Create your views here.
class LineLoginView(LoginRequiredMixin,View):
    def get(self,request,line_id):
        a = LineAccount(username=request.user,line_id=line_id)
        a.save()
        push_message(line_id,"ログインに成功しました！")
        return HttpResponse('success')


class LineView(View):
    def post(self,request):
        req = json.loads(request.body.decode('utf-8'))
        events = req['events']
        for event in events:
            line_bot = LineBot(event)
            if event["type"] == "message":
                line_bot.message_event(event["message"]["text"])
            elif  event["type"] == "follow":
                line_bot.follow_event()
            elif  event["type"] == "postback":
                line_bot.postback_event()
            else:
                pass
        return HttpResponse(status=200)
        