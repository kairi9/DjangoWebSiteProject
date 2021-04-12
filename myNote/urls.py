from django.urls import path
from . import views

app_name = "myNote"
urlpatterns = [
    #todo
    path('',views.MyPage.as_view(),name='myPage'),
    path('ajax_view/',views.ajax_view,name='ajview'),
    path('schedule_view/',views.DateScheduleAjax.as_view(),name='schedule'),
    path('sche_change/',views.ChangeScheduleAjax.as_view(),name='change'),
    path('sche_change/<int:id>/',views.change_sche_view,name='change_post'),
    path('sche_del/',views.DelScheduleAjax.as_view(),name='del'),
    path('sche_del/<int:id>/',views.del_sche_view,name='del_post'),
    #note
    path('note/',views.Note.as_view(),name='note'),
]