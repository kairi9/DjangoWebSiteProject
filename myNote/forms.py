from django import forms
from .models import CalendarToDo

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

class GetCodeAsFileForm(forms.Form):
    code_file = forms.FileField()
    discription = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'cols':30}))