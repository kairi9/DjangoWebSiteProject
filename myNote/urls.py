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
    #task
    path('task/',views.TaskView.as_view(),name='task'),
    path('task/<int:id>/',views.task_done,name='task_done'),
    #note
    path('note/',views.Note.as_view(),name='note'),
    path('note/upload_file/',views.file_upload_view,name='upload_file'),
    path('note/codes/',views.Editor.as_view(),name='codes'),
    path('note/codes/<int:id>/',views.Editor.as_view(),name='show_codes'),
    path('note/codes/<int:id>/delete/',views.del_code,name='del_codes'),
    path('note/find_code/',views.FindCodeView.as_view(),name='find_codes'),
    path('note/find_code/<int:id>/',views.FoundCodeView.as_view(),name='found_code'),
    #line
    path('line_qr/',views.LineAccountAddView.as_view(),name='line'),
]