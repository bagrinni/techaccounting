from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from records.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),

    # Авторизация
    path('login/', auth_views.LoginView.as_view(template_name='records/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),

    # Подключаем urls.py из приложения records
    path('', include('records.urls')),  # Главная и все остальные маршруты

    # Опционально: можно перенаправить /home/ на login, но лучше убрать этот путь
]
