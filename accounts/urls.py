from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import MyLoginForm

app_name = "accounts"
urlpatterns = [
    path('create_account/',views.Create_account.as_view(),name='create'),
    path('login/',auth_views.LoginView.as_view(
        form_class=MyLoginForm,
        template_name='accounts/login.html',
    ),name="login"),
    path('logout/',auth_views.LogoutView.as_view(),name='logout')
]