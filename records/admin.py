from django.contrib import admin
from .models import Department, PhoneRecord

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name')  # Какие поля отображать в списке
    search_fields = ('name', 'short_name')  # Поля для поиска

@admin.register(PhoneRecord)
class PhoneRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_4', 'phone_6', 'department', 'port_asl', 'stan', 'lin', 'status_id')
    search_fields = ('phone_4', 'phone_6', 'department__name')
    list_filter = ('department', 'status_id')  # Фильтры справа
    ordering = ('phone_6',)

    def save_model(self, request, obj, form, change):
        """ Автоматически формируем 6-значный номер перед сохранением """
        if obj.phone_4 and not obj.phone_6:
            obj.phone_6 = f"{obj.DEFAULT_PREFIX}{obj.phone_4}"
        super().save_model(request, obj, form, change)


from django.contrib import admin
from .models import DamageRecord

@admin.register(DamageRecord)
class DamageRecordAdmin(admin.ModelAdmin):
    list_display = ('phone_record', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('phone_record__phone_4', 'phone_record__phone_6', 'comment')
    ordering = ('-created_at',)

