from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from  django.views.generic import CreateView
from .forms import MyUserCreateForm,MyLoginForm
# Create your views here.

#ログインページ
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


#アカウント作成
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = MyUserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            full_name = form.cleaned_data.get('full_name')
            user = authenticate(username=username, full_name=full_name, password=password)
            login(request, user)
            return redirect('/login')
        return render(request,'accounts/create.html',{'form':form,})
    def get(self, request, *args, **kwargs):
        form = MyUserCreateForm(request.POST)
        return render(request,'accounts/create.html',{'form':form,})