from django.contrib import admin
from .models import MyCodes, CalendarToDo,Task, ProgrammingLanguage #importするものを記述

# Register your models here.
admin.site.register(MyCodes)
admin.site.register(CalendarToDo)
admin.site.register(Task)
admin.site.register(ProgrammingLanguage)