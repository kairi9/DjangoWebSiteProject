from django import forms
from .models import CalendarToDo,Task,MyCodes

#schedule
class DateScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.input_type = 'time'
        self.fields['end_time'].widget.input_type = 'time'
        self.fields['date'].widget.input_type = 'date'
        self.fields['discription'].widget = forms.Textarea(attrs={'rows':1, 'cols':15})

    class Meta:
        model = CalendarToDo
        fields = ['title','start_time','end_time','date','done','discription']


#note
class GetCodeAsFileForm(forms.Form):
    code_file = forms.FileField()
    discription = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'cols':30}))

class CodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs["form"] = "code_form"
        self.fields['extension'].widget.attrs["form"] = "code_form"
        self.fields['discription'].widget = forms.Textarea(attrs={'rows':1, 'cols':15, 'form':'code_form'})
        self.fields['code'].widget = forms.Textarea(attrs={'rows':1, 'cols':15, 'form':'code_form'})
    class Meta:
        model = MyCodes
        fields = ['title','code','extension','discription']

class FindCodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['extension'].widget.attrs["form"] = "find_form"
    class Meta:
        model = MyCodes
        fields = ['extension']

#task
class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_time'].widget.input_type = 'time'
        self.fields['date'].widget.input_type = 'date'
        self.fields['discription'].widget = forms.Textarea(attrs={'rows':1, 'cols':15})
        
    class Meta:
        model = Task
        fields = ['title','date','end_time','discription']