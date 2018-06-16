from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic


def index(request):
    current_list_list = List.objects.order_by('id', 'list_name')
    full_list = {}
    for list in current_list_list:
        full_list[list] = []
        current_task_list = Task.objects.filter(list_id=list.id).filter(completed=False).order_by(
            '-list_id') \
            .order_by('-due_date')
        for task in current_task_list:
            full_list[list].append(task)
    output = {'full_list': full_list}
    return render(request, 'my_todos/index.html', output)


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'my_todos/task.html', {'task': task})


class ListDetail(generic.DetailView):
    model = List


class ListLists(generic.ListView):
    model = List
