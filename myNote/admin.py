from django.contrib import admin
from .models import MyCodes, CalendarToDo #importするものを記述

# Register your models here.
admin.site.register(MyCodes)
admin.site.register(CalendarToDo)