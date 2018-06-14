import datetime
from django.db import models
from django.utils import timezone
# Create your models here.


class List(models.Model):
    list_name = models.CharField(max_length=200)

    def __str__(self):
        return self.list_name


class Task(models.Model):
    list_id = models.ForeignKey(List, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    pub_date = models.DateField('date created')
    due_date = models.DateField('date due')
    description = models.TextField(max_length=1000)
    completed = models.BooleanField()

    def due_soon(self):
        return self.due_date >= timezone.now() - datetime.timedelta(days=2)

    def __str__(self):
        return self.task_name
