from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from  django.views.generic import CreateView
from .forms import MyUserCreateForm,MyLoginForm
from .models import MyUser
from django.urls import reverse_lazy
# Create your views here.

#ログインページ
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


#アカウント作成
class Create_account(CreateView):
    model = MyUser
    template_name = 'accounts/create.html'
    form_class = MyUserCreateForm
    success_url=reverse_lazy('accounts:login')