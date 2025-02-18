from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),  # Главная страница

    # Страницы с записями
    path('records/', views.PhoneRecordListView.as_view(), name='phone-record-list'),
    path('records/<int:pk>/edit/', views.edit_phone_record, name='phone-record-edit'),
    path('records/delete/', views.PhoneRecordDeleteView.as_view(), name='phone-record-delete'),

    # Записи по отделам
    path('department/<int:department_id>/', views.DepartmentPhoneRecordListView.as_view(), name='department-phone-record-list'),

    # Номера, не привязанные к организации
    path('population/', views.PopulationPhoneRecordListView.as_view(), name='population-phone-record-list'),

    # Повреждения
    path('damage/', views.DamageRecordCreateView.as_view(), name='damage-record-add'),

    # Организации (исправил `departmens` → `departments`)
    path('departmens/', views.OrganizationListView.as_view(), name='departmens-list')


]
