from django.db import models
import datetime
from django.contrib.auth import get_user_model
# Create your models here.


class LineAccount(models.Model):
  username = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
  )
  line_id = models.CharField(max_length=150)
  date = models.DateField(auto_now=False,auto_now_add=True)

  def __str__(self):
    return self.line_id