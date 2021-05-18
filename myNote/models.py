from django.db import models
import datetime
from django.contrib.auth import get_user_model
# Create your models here.

class ProgrammingLanguage(models.Model):
  language = models.CharField(max_length=50)
  extension = models.CharField(max_length=50)
  path_to_file = models.CharField(max_length=50)

  def __str__(self):
    return self.language

class MyCodes(models.Model):
  username = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
  )
  title = models.CharField(max_length=50)
  code = models.TextField()
  extension = models.ForeignKey(
    ProgrammingLanguage,
    on_delete=models.CASCADE,
  )
  discription = models.TextField()
  date = models.DateField(auto_now=True,auto_now_add=False)

  def __str__(self):
    return self.title
  
  def get_extension(self):
    return self.title.split('.')[-1]


class CalendarToDo(models.Model):
  username = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
  )
  title = models.CharField(max_length=50)
  start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
  end_time = models.TimeField('終了時間', default=datetime.time(12, 0, 0))
  date = models.DateField()
  done = models.BooleanField(default=False)
  discription = models.CharField(max_length=100)

  def __str__(self):
      return self.title


class Task(models.Model):
  username = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
  )
  title = models.CharField(max_length=50)
  end_time = models.TimeField('期限', default=datetime.time(23, 59))
  date = models.DateField(default=datetime.date.today)
  done = models.BooleanField(default=False)
  expired = models.BooleanField(default=False)
  today = models.BooleanField(default=False)
  discription = models.CharField(max_length=100,default='なし')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if not self.date is None:
      if self.return_deadline() > 0:
        self.expired = False
        self.today = False
      elif self.return_deadline() < 0:
        self.expired = True
        self.today = False
      else:
        self.expired = False
        self.today = True

  def __str__(self):
      return self.title
  
  def return_deadline(self):
    today = datetime.date.today()
    deadline = self.date - today
    return deadline.days