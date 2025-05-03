from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Subject, Task, Question
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class SubjectListView(ListView):
    model = Subject
    template_name = 'tasks/subject_list.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        for subject in context['subjects']:
            subject.days_until_exam = (subject.exam_date - today).days
            subject.task_count = Task.objects.filter(subject=subject).count()
            subject.completed_tasks = Task.objects.filter(subject=subject, completed=True).count() 
        return context

class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'tasks/subject_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.object
        tasks = subject.task_set.all().order_by('order')
        completed_tasks_count = subject.task_set.filter(completed=True).count()
        today = timezone.now().date()

        # Добавляем days_until как атрибут объекта subject
        subject.days_until = (subject.exam_date - today).days
        subject.completed_tasks = completed_tasks_count
        subject.task_count = tasks.count()
        context.update({
            "exam_date": subject.exam_date,
            'tasks': tasks,
            'completed_tasks_count': completed_tasks_count,
        })
        return context
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    slug_url_kwarg = 'subject_slug'
    
    def get_object(self, queryset=None):
        subject_slug = self.kwargs.get('subject_slug')
        task_number = self.kwargs.get('task_number')
        subject = get_object_or_404(Subject, slug=subject_slug)
        return get_object_or_404(Task, subject=subject, order=task_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object

        # Преобразование ссылки YouTube в формат для встраивания
        if task.video_url:
            if "youtube.com/watch" in task.video_url:
                video_id = task.video_url.split("v=")[-1].split("&")[0]
                task.video_url = f"https://www.youtube.com/embed/{video_id}"
            elif "youtu.be/" in task.video_url:
                video_id = task.video_url.split("youtu.be/")[-1]
                task.video_url = f"https://www.youtube.com/embed/{video_id}"
        
        context.update({
            'subject': task.subject,
            'tasks': task.subject.task_set.order_by('order'),
            'questions': task.question_set.filter(task=task).order_by('id'),
            'today': timezone.now().date(),
            'image': task.image,
            'pdf': task.pdf,
            'video_url': task.video_url,
        })
        return context
@csrf_exempt
def toggle_task_completion(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = not task.completed  # Переключаем состояние
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed})
    return JsonResponse({'success': False}, status=400)