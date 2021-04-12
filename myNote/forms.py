from django.forms import ModelForm
from .models import CalendarToDo
class DateScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.input_type = 'time'
        self.fields['end_time'].widget.input_type = 'time'
        self.fields['date'].widget.input_type = 'date'

    class Meta:
        model = CalendarToDo
        fields = ['title','start_time','end_time','date','done','discription']