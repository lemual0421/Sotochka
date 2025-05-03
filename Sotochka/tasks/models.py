from django.db import models
from django.utils.text import slugify

class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    exam_date = models.DateField()
    slug = models.SlugField(max_length=200, unique=True, default=('hah'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Task(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)  # Для текста с формулами
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    topic = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        unique_together = ['subject', 'order']

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Текстовый ответ'),
        ('number', 'Числовой ответ'),
        ('matrix', 'Матрица'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    question_text= models.TextField()
    correct_answer = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
def mathjax(request):
    return {'mathjax': True}