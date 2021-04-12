from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View
import json
from .linebot import LineBot
from .models import LineAccount
from django.contrib.auth import views as auth_views
from accounts.forms import MyLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class LineLoginView(LoginRequiredMixin,View):
    def get(self,request,line_id):
        a = LineAccount(username=request.user,line_id=line_id)
        a.save()
        return HttpResponse('success')


class LineView(View):
    def get(self,request):
        
        return HttpResponse()

    def post(self,request):
        req = json.loads(request.body.decode('utf-8'))
        events = request['events']
        for event in events:
            line_bot = LineBot(event)
        return redirect('/')