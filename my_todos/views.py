from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.


def index(request):
    latest_task_list = Task.objects.order_by('-due_date')[:5]
    output = {'latest_task_list' : latest_task_list}
    return render(request, 'my_todos/index.html', output)


def detail(request, task_id):
    return HttpResponse("You be looking at task %s." % task_id)
