from django.contrib import admin
from django.utils.html import format_html
from .models import Subject, Task, Question, StudyMaterial

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('question_text', 'question_type', 'correct_answer', 'image')
    show_change_link = True
    classes = ('collapse',)  # Добавляем возможность сворачивать инлайн

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'pdf')  # Поля, которые будут отображаться в списке
    list_filter = ('subject',)  # Фильтры справа
    search_fields = ('name', 'description')  # Поля, по которым можно будет искать

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('title', 'topic', 'order', 'completed')
    show_change_link = True
    readonly_fields = ('completed',)  # Статус выполнения только для чтения
    classes = ('collapse',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_date', 'task_count')
    list_filter = ('exam_date',)
    search_fields = ('name', 'description')
    inlines = [TaskInline]
    ordering = ('exam_date', 'name')
    list_per_page = 20
    
    # Добавляем количество задач в списке предметов
    def task_count(self, obj):
        return obj.task_set.count()
    task_count.short_description = 'Кол-во задач'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject_name', 'topic', 'order', 'completed', 'has_pdf', 'has_image', 'question_count')
    list_filter = ('subject', 'topic', 'completed')
    search_fields = ('title', 'content', 'subject__name')
    inlines = [QuestionInline]
    ordering = ('subject', 'order')
    list_per_page = 30
    list_editable = ('completed', 'order')  # Быстрое редактирование прямо в списке
    
    # Для удобного отображения связанных файлов
    readonly_fields = ('preview_pdf', 'preview_image', 'question_count')
    fieldsets = (
        (None, {
            'fields': ('subject', 'title', 'topic', 'order', 'completed')
        }),
        ('Содержание', {
            'fields': ('content',)
        }),
        ('Медиафайлы', {
            'fields': ('pdf', 'preview_pdf', 'image', 'preview_image', 'video_url'),
            'classes': ('collapse',)
        }),
    )
    
    # Кастомизация отображения названия предмета
    def subject_name(self, obj):
        return obj.subject.name
    subject_name.short_description = 'Предмет'
    subject_name.admin_order_field = 'subject__name'  # Сортировка по имени предмета
    
    # Превью PDF
    def preview_pdf(self, obj):
        if obj.pdf:
            return format_html(
                '<a href="{}" target="_blank" class="button">Просмотреть PDF</a>',
                obj.pdf.url
            )
        return "-"
    preview_pdf.short_description = "PDF файл"
    
    # Превью изображения
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px;" />',
                obj.image.url
            )
        return "-"
    preview_image.short_description = "Превью изображения"
    
    # Индикаторы наличия файлов в списке
    def has_pdf(self, obj):
        return bool(obj.pdf)
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Изображение'
    
    # Количество вопросов
    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = 'Вопросы'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_question_text', 'task_with_subject', 'question_type', 'correct_answer_preview', 'image')
    list_filter = ('question_type', 'task__subject')
    search_fields = ('question_text', 'correct_answer', 'task__title')
    ordering = ('task__subject', 'task', 'id')
    list_per_page = 30
    
    # Группировка полей
    fieldsets = (
        (None, {
            'fields': ('task', 'question_type', )
        }),
        ('Вопрос и ответ', {
            'fields': ('image','question_text', 'correct_answer')
        }),
    )
    
    # Короткий текст вопроса для списка
    def short_question_text(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    short_question_text.short_description = 'Вопрос'
    
    # Задача с указанием предмета
    def task_with_subject(self, obj):
        return f"{obj.task.subject.name}: {obj.task.title}"
    task_with_subject.short_description = 'Задача'
    task_with_subject.admin_order_field = 'task__subject__name'
    
    # Превью правильного ответа
    def correct_answer_preview(self, obj):
        return obj.correct_answer[:30] + '...' if len(obj.correct_answer) > 30 else obj.correct_answer
    correct_answer_preview.short_description = 'Правильный ответ'

# Добавляем кастомизацию заголовка админки
admin.site.site_header = 'Администрирование онлайн-школы'
admin.site.site_title = 'Онлайн-школа'
admin.site.index_title = 'Управление учебными материалами'