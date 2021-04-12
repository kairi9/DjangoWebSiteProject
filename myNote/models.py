from django.db import models
import datetime
from django.contrib.auth import get_user_model
# Create your models here.


class MyCodes(models.Model):
  username = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
  )
  title = models.CharField(max_length=50)
  code = models.TextField()
  discription = models.TextField()
  date = models.DateField(auto_now=True,auto_now_add=False)

  def __str__(self):
    return self.title


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
  