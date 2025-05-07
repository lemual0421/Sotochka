from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject_list'),
    path('subject/<slug:slug>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('task/<slug:subject_slug>/<int:task_number>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:task_id>/toggle/', views.toggle_task_completion, name='toggle_task_completion'),
]