from django.shortcuts import render,get_object_or_404,redirect
from .models import MyCodes, CalendarToDo,Task,ProgrammingLanguage
from .my_calendar import MyCalendar,get_todays_datail
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import DateScheduleForm,GetCodeAsFileForm,TaskForm,CodeForm
from datetime import date


#トップページ
class MyPage(LoginRequiredMixin,TemplateView):
    #テンプレートのパス
    template_name = 'myNote/index.html'
    redirect_field_name = 'redirect_to'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.get_username
        context['username']=username
        form = DateScheduleForm(initial={'username':self.request.user})
        context['form'] = form
        return context



#カレンダーAjax処理用
@login_required(redirect_field_name='myNote:myPage')
def ajax_view(request):
    if request.method == 'GET':  # GETの処理
        #カレンダーを返す
        year = int(request.GET.get("year"))
        month = int(request.GET.get("month"))
        calendar = MyCalendar(request,year,month)
        return HttpResponse(calendar.formatmonth())
    elif request.method == 'POST':  # POSTの処理
        return redirect('myNote:ajview')

#カレンダー詳細Ajax処理用
class DateScheduleAjax(LoginRequiredMixin,View):
    template_name = 'myNote/index.html'
    redirect_field_name = 'redirect_to'

    #指定日の予定取得処理
    def get(self,request):
        day = int(request.GET.get("day"))
        year = int(request.GET.get("year"))
        month = int(request.GET.get("month"))
        day1 = date(year,month,day).isoformat()
        datas = get_todays_datail(request,day1)
        if len(datas) == 0:
            context = "<p>予定はありません。</p>"
        else:
            context = "<h3>{}月{}日の予定</h3>".format(month,day)
            context += "<div class='sche_titles'><ul>"
            for i,d in enumerate(datas):
                context += "<li onclick='sche_click(this,{})'>{}</li>".format(i+1,d['title'])
            context += "</ul></div>"
            japanese_dict = {
                'title':'やること',
                'start_time':'開始時間',
                'end_time':'終了時刻',
                'date':'日付',
                'done':'DONE',
                'discription':'やること詳細',
            }
            context += "<div id='sche_table'>"
            for d in datas:
                #form = DateScheduleForm(request.GET or None, initial=d)
                context += "<table border='0' cellpadding='0' cellspacing='0' class='no_disp' >"
                for key,item in d.items():
                    if key=='start_time' or key=='end_time':
                        item = ('{}:{}').format(item.hour,(str(item.minute)).zfill(2))
                    elif key=='id':
                        continue
                    context += "<tr><th>{}</th><td>{}</td></tr>".format(japanese_dict[key],item)
                context += "<tr><td><button class='change-btn' onclick='sche_change({})'>変更</button></td><td><button class='delete-btn' onclick='sche_del({})'>削除</button></td></tr>".format(d['id'],d['id'])
                context += "</table>"
            context += "</div>"
        return HttpResponse(context)
    
    #新規予定追加処理
    def post(self,request):
        a = CalendarToDo()
        a.username = request.user
        f = DateScheduleForm(request.POST,instance=a)
        if f.is_valid():
            f.save()
        return redirect('myNote:myPage')

#予定変更確認用
class ChangeScheduleAjax(LoginRequiredMixin,View):
    template_name = 'myNote/index.html'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        try:
            data = CalendarToDo.objects.filter(username=request.user,id=request.GET.get("id"))
        except:
            data = ""
        japanese_dict = {
            'title':'やること',
            'start_time':'開始時間',
            'end_time':'終了時刻',
            'date':'日付',
            'done':'DONE',
            'discription':'やること詳細',
        }
        context = ""
        for d in data:
            context += "<tr><th>{}</th><td><input type='text' name='title' maxlength='50' required='' id='id_title' value='{}' ></td></tr>".format(japanese_dict['title'],d.title)
            context += "<tr><th>{}</th><td><input type='time' name='start_time' value='{}' required='' id='id_start_time'></td></tr>".format(japanese_dict['start_time'],d.start_time)
            context += '<tr><th>{}</th><td><input type="time" name="end_time" value="{}" required="" id="id_end_time"></td></tr>'.format(japanese_dict['end_time'],d.end_time)
            context += '<tr><th>{}</th><td><input type="date" name="date" required="" id="id_date" value="{}"></td></tr>'.format(japanese_dict['date'],d.date)
            if d.done:
                context += '<tr><th>{}</th><td><input type="checkbox" name="done" id="id_done" checked ></td></tr>'.format(japanese_dict['done'])
            else:
                context += '<tr><th>{}</th><td><input type="checkbox" name="done" id="id_done" ></td></tr>'.format(japanese_dict['done'])
            context += '<tr><th>{}</th><td><input type="text" name="discription" maxlength="100" value="{}" required="" id="id_discription"></td></tr>'.format(japanese_dict['discription'],d.discription)
            context += '<tr><td><input type="submit" value="変更" ></td><td><input type="button" value="キャンセル" onclick="cancel()"></td></tr>'
        return HttpResponse(context)

    def post(self,request):
        return redirect('myNote:change')

#予定削除確認用
class DelScheduleAjax(LoginRequiredMixin,View):
    template_name = 'myNote/index.html'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        try:
            data = CalendarToDo.objects.filter(username=request.user,id=request.GET.get("id"))
        except:
            data = ""
        japanese_dict = {
            'title':'やること',
            'start_time':'開始時間',
            'end_time':'終了時刻',
            'date':'日付',
            'done':'DONE',
            'discription':'やること詳細',
        }
        context = ""
        for d in data:
            context += "<tr><th>{}</th><td>{}</td></tr>".format(japanese_dict['title'],d.title)
            context += "<tr><th>{}</th><td>{}</td></tr>".format(japanese_dict['start_time'],d.start_time)
            context += '<tr><th>{}</th><td>{}</td></tr>'.format(japanese_dict['end_time'],d.end_time)
            context += '<tr><th>{}</th><td>{}</td></tr>'.format(japanese_dict['date'],d.date)
            context += '<tr><th>{}</th><td>{}</td></tr>'.format(japanese_dict['done'],d.done)
            context += '<tr><th>{}</th><td>{}</td></tr>'.format(japanese_dict['discription'],d.discription)
            context += '<tr><td><input type="submit" value="削除" ></td><td><input type="button" value="キャンセル" onclick="cancel()"></td></tr>'
        return HttpResponse(context)
    
    def post(self,request):
        return redirect('myNote:del')

#予定変更処理用
@login_required(redirect_field_name='myNote:myPage')
def change_sche_view(request,id):
    if request.method == 'GET':  # GETの処理
        redirect('myNote:myPage')
    elif request.method == 'POST':  # POSTの処理
        obj = CalendarToDo.objects.get(username=request.user,id=id)
        f = DateScheduleForm(request.POST,instance=obj)
        f.save()
        return redirect('myNote:myPage')

#予定削除処理用
@login_required(redirect_field_name='myNote:myPage')
def del_sche_view(request,id):
    if request.method == 'GET':  # GETの処理
        redirect('myNote:myPage')
    elif request.method == 'POST':  # POSTの処理
        obj = CalendarToDo.objects.get(username=request.user,id=id)
        obj.delete()
        return redirect('myNote:myPage')

#ノート
class Note(LoginRequiredMixin,TemplateView):
    #テンプレートのパス
    template_name = 'myNote/note.html'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        data = MyCodes.objects.filter(username=request.user).order_by('date')[:10]
        form = GetCodeAsFileForm()
        context = {
            'datas':data,
            'form':form
        }
        return render(request,'myNote/note.html',context)
    
    def post(self,request, *args, **kwargs):
        return redirect('myNote:note')

class Editor(LoginRequiredMixin,TemplateView):
    #テンプレートのパス
    template_name = 'myNote/editor.html'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('id') is not None:
            obj = MyCodes.objects.get(username=self.request.user,id=self.kwargs.get('id'))
            form = CodeForm(initial={
                'title':obj.title,
                'extension':obj.extension,
                'discription':obj.discription,
            })
            context['code'] = obj.code
        else:
            form = CodeForm()
            context['code'] = "//コード"
        context['form'] = form
        data = MyCodes.objects.filter(username=self.request.user).order_by('date')[:5]
        context['datas'] = data
        return context

    def post(self,request, *args, **kwargs):
        obj = MyCodes(username=request.user,code=request.POST['codemirror'])
        form = CodeForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
        return redirect('myNote:note')

#コードファイルアップロード用
@login_required(redirect_field_name='myNote:myPage')
def file_upload_view(request):
    if request.method == 'POST':
        form = GetCodeAsFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.cleaned_data['code_file']
            discription = form.cleaned_data['discription']
            with file_obj.open(mode='r') as f:
                code = f.read().decode('utf-8')
            extension = file_obj.name.split('.')[-1]
            language_obj = ProgrammingLanguage.objects.get(extension=extension)
            obj = MyCodes(username=request.user,title=file_obj.name,code=code,extension=language_obj,discription=discription)
            obj.save()
            return redirect('myNote:note')
        else:
            return HttpResponse('処理失敗')



#task
class TaskView(LoginRequiredMixin,TemplateView):
    template_name = 'myNote/task.html'
    redirect_field_name = 'redirect_to'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taskes = Task.objects.filter(username=self.request.user,done=False).order_by('date')[:16]
        form = TaskForm(initial={'username':self.request.user})
        context['taskes']=taskes
        context['form']=form
        return context
    
    def post(self,request):
        obj = Task()
        obj.username = request.user
        form = TaskForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
        return redirect('myNote:task')

@login_required(redirect_field_name='myNote:task')
def task_done(request,id):
    if request.method == 'GET':
        obj = Task.objects.get(username=request.user,id=id)
        obj.done = True
        obj.save()
        return redirect('myNote:task')