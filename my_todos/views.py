from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from copy import deepcopy


def home(request):
    current_list_list = List.objects.order_by('id', 'list_name')
    full_list = {}
    for list in current_list_list:
        full_list[list] = []
        current_task_list = Task.objects.filter(list_id=list.id).\
            filter(completed=False).\
            filter(Q(due_date=datetime.date.today()) | (Q(due_date=None) and Q(persistent=True))).\
            filter(Q(parent_task__isnull=True) | Q(parent_task__enforce=False)).\
            order_by('-list_id').\
            order_by('-due_date')
        for task in current_task_list:
            full_list[list].append(task)
    output = {'full_list': full_list}
    return render(request, 'my_todos/home.html', output)


def home_tomorrow(request):
    current_list_list = List.objects.order_by('id', 'list_name')
    full_list = {}
    for list in current_list_list:
        full_list[list] = []
        current_task_list = Task.objects.filter(list_id=list.id). \
            filter(completed=False). \
            filter(Q(due_date=datetime.date.today()+datetime.timedelta(days=1)) | (Q(due_date=None) and Q(persistent=True))). \
            filter(Q(parent_task__isnull=True) | Q(parent_task__enforce=False)). \
            order_by('-list_id'). \
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


def task_complete(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = True
    task.save()
    if task.recurring:
        task2 = deepcopy(task)
        task2.id = None
        task2.due_date = datetime.date.today() + datetime.timedelta(days=1)
        task2.completed = False
        task2.save()
    for depend in Dependancy.objects.filter(child_id=task.id):
        depend.enforce = False
        depend.save()
    return redirect(reverse('todos:home'))


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


class DependancyDetail(generic.DetailView):
    model = Dependancy


class DependancyList(generic.ListView):
    model = Dependancy

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
    fields = ['task_name', 'pub_date', 'due_date', 'description', 'list_id', 'recurring', 'persistent', 'completed']


class TaskDelete(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('todos:home')


class DependancyCreate(generic.CreateView):
    model = Dependancy
    fields = ['parent_id', 'child_id']


class DependancyUpdate(generic.UpdateView):
    model = Dependancy
    fields = ['parent_id', 'child_id', 'enforce']


class DependancyDelete(generic.DeleteView):
    model = Dependancy
    success_url = reverse_lazy('todos:home')