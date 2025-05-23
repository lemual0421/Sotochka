from django.urls import path
from . import views

app_name = 'accounts'  # Убедитесь, что namespace указан

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),  # Убедитесь, что маршрут для профиля существует
]
