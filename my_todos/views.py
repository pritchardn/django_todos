from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic
from django.urls import reverse_lazy


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


class TaskDetail(generic.DetailView):
    model = Task


class ListDetail(generic.DetailView):
    model = List


class ListLists(generic.ListView):
    model = List

# Forms --------------------------------------


class ListCreate(generic.CreateView):
    model = List
    fields = ['list_name']


class ListUpdate(generic.UpdateView):
    model = List
    fields = ['list_name']


class ListDelete(generic.DeleteView):
    model = List
    success_url = reverse_lazy('todos:index')


class TaskCreate(generic.CreateView):
    model = Task
    fields = ['task_name', 'pub_date', 'due_date', 'description', 'list_id', 'recurring', 'persistent']


class TaskUpdate(generic.UpdateView):
    model = Task
    fields = ['task_name', 'pub_date', 'due_date', 'description', 'recurring', 'persistent']


class TaskDelete(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('todos:index')

