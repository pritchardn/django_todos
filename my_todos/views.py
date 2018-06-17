from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q


def home(request):
    current_list_list = List.objects.order_by('id', 'list_name')
    full_list = {}
    for list in current_list_list:
        full_list[list] = []
        current_task_list = Task.objects.filter(list_id=list.id).\
            filter(completed=False).\
            filter(Q(due_date__gte=datetime.date.today()) | Q(due_date=None)).\
            order_by('-list_id').\
            order_by('-due_date')
        for task in current_task_list:
            full_list[list].append(task)
    output = {'full_list': full_list}
    return render(request, 'my_todos/home.html', output)


def home_completed(request):
    current_list_list = List.objects.order_by('id', 'list_name')
    full_list = {}
    for list in current_list_list:
        full_list[list] = []
        current_task_list = Task.objects.filter(list_id=list.id).filter(completed=True).order_by(
            '-list_id') \
            .order_by('-due_date')
        for task in current_task_list:
            full_list[list].append(task)
    output = {'full_list': full_list}
    return render(request, 'my_todos/home.html', output)


def home_all(request):
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
    return render(request, 'my_todos/home.html', output)


def home_overdue(request):
    current_list_list = List.objects.order_by('id', 'list_name')
    full_list = {}
    for list in current_list_list:
        full_list[list] = []
        current_task_list = Task.objects.filter(list_id=list.id).\
            filter(completed=False).\
            filter(due_date__lt=datetime.date.today()).\
            order_by('-list_id').\
            order_by('-due_date')
        for task in current_task_list:
            full_list[list].append(task)
    output = {'full_list': full_list}
    return render(request, 'my_todos/home.html', output)


class TaskDetail(generic.DetailView):
    model = Task


class ListSummary(generic.ListView):
    model = List

    def get_queryset(self):
        return Task.objects.filter(list_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['list'] = List.objects.get(pk=self.kwargs['pk'])
        return context

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
    success_url = reverse_lazy('todos:home')


class TaskCreate(generic.CreateView):
    model = Task
    fields = ['task_name', 'pub_date', 'due_date', 'description', 'list_id', 'recurring', 'persistent']


class TaskUpdate(generic.UpdateView):
    model = Task
    fields = ['task_name', 'pub_date', 'due_date', 'description', 'recurring', 'persistent']


class TaskDelete(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('todos:home')

