from django.urls import path
from . import views




app_name = "lineapp"
urlpatterns = [
    path('',views.LineView.as_view(),name='linebot'),
    path('login/<str:line_id>/',views.LineLoginView.as_view(),name="login"),
]
