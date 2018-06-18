from django.urls import path
from . import views
from my_todos.views import *
from django.conf.urls import url

app_name = 'todos'

urlpatterns = [
    # Overviews
    path('home/', views.home, name='home'),
    path('home/completed', views.home_completed, name='home_completed'),
    path('home/all', views.home_all, name='home_all'),
    path('home/overdue', views.home_overdue, name='home_overdue'),
    # Lists
    path('list/<int:pk>/', ListSummary.as_view(), name='list_summary'),
    path('list/new/', ListCreate.as_view(), name='list_new'),
    path('list/<int:pk>/update/', ListUpdate.as_view(), name='list_update'),
    path('list/<int:pk>/delete/', ListDelete.as_view(), name='list_delete'),
    # Tasks
    path('task/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('task/new/', TaskCreate.as_view(), name='task_new'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('task/<int:task_id>/complete/', views.task_complete, name='task_complete')
    # Management
]
