from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.


def index(request):
    current_list_list = List.objects.order_by('id', 'list_name')
    current_task_list = Task.objects.filter(list_id__in=current_list_list).filter(completed=False).order_by('-list_id') \
        .order_by('-due_date')
    full_list = {}
    for list in current_list_list:
        full_list[list.list_name] = []
    for task in current_task_list:
        full_list[task.list_id.list_name].append(task)
    output = {'full_list': full_list}
    return render(request, 'my_todos/index.html', output)


def detail(request, task_id):
    return HttpResponse("You be looking at task %s." % task_id)
