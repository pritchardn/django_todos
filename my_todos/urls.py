from django.urls import path
from . import views
from my_todos.views import *
from django.conf.urls import url

app_name = 'todos'

urlpatterns = [
    path('', views.index, name='index'),
    path('task/<int:task_id>/', views.task_detail, name='detail'),
    url(r'^lists/$', ListLists.as_view()),
    path('list/<int:pk>', ListDetail.as_view())
]