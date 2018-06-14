from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Henlo world, welcome to my todolist")


def detail(request, task_id):
    return HttpResponse("You be looking at task %s." % task_id)
