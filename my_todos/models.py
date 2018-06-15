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
    completed = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)
    persistent = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name


class Dependancy(models.Model):
    parent_id = models.ForeignKey(Task, related_name='parent_task', on_delete=models.CASCADE)
    child_id = models.ForeignKey(Task, related_name='child_task', on_delete=models.CASCADE)

    def __str__(self):
        return "Parent: " + self.parent_id.task_name + " Child: " + self.child_id.task_name
