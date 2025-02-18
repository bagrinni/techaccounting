from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, TemplateView, View
from django.urls import reverse_lazy
from django.db.models import Q
from .models import PhoneRecord, Department, DamageRecord
from .forms import PhoneRecordForm
from .mixins import TechMechanicRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Главная страница
class HomePageView(TemplateView):
    template_name = "records/home.html"


# Страница списка записей телефонов
class PhoneRecordListView(ListView):
    model = PhoneRecord
    template_name = 'records/phone_record_list.html'
    context_object_name = 'phone_records'
    paginate_by = 25  # 25 записей на страницу

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['can_edit'] = user.is_authenticated and (user.is_superuser or user.groups.filter(name="Механники тех учета").exists())
        context['create_form'] = PhoneRecordForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        phone = self.request.GET.get('phone')
        port_asl = self.request.GET.get('port_asl')
        lin = self.request.GET.get('lin')
        
        # Фильтрация по введенным параметрам
        if phone:
            queryset = queryset.filter(phone_4__icontains=phone) | queryset.filter(phone_6__icontains=phone)
        if port_asl:
            queryset = queryset.filter(port_asl__icontains=port_asl)
        if lin:
            queryset = queryset.filter(lin__icontains=lin)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        # Пагинация
        paginator = Paginator(self.object_list, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            records = []
            for record in page_obj:
                records.append({
                    'id': record.id,
                    'phone_4': record.phone_4,
                    'phone_6': record.phone_6,
                    'department': str(record.department) if record.department else '',
                    'port_asl': record.port_asl,
                    'stan': record.stan,
                    'lin': record.lin,
                })
            return JsonResponse({'records': records})

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not (user.is_authenticated and (user.is_superuser or user.groups.filter(name="Механники тех учета").exists())):
            return JsonResponse({'error': 'Нет прав для создания записи.'}, status=403)
        
        form = PhoneRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Запись успешно добавлена'})
        return JsonResponse({'error': 'Ошибка при добавлении записи'}, status=400)


# Редактирование записи телефона
@login_required
def edit_phone_record(request, pk):
    record = get_object_or_404(PhoneRecord, pk=pk)
    if not (request.user.is_superuser or request.user.groups.filter(name="Механники тех учета").exists()):
        return HttpResponseForbidden("У вас нет доступа к редактированию записей.")
    
    if request.method == "POST":
        form = PhoneRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('phone-record-list')
    else:
        form = PhoneRecordForm(instance=record)
    
    return render(request, 'records/inline_edit_phone_record.html', {'form': form, 'record': record})


# Удаление записи телефона
class PhoneRecordDeleteView(View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not (user.is_authenticated and (user.is_superuser or user.groups.filter(name="Механники тех учета").exists())):
            return JsonResponse({'error': 'Нет прав для удаления записи.'}, status=403)
        
        record_id = request.POST.get('id')
        try:
            record = PhoneRecord.objects.get(id=record_id)
            record.delete()
            return JsonResponse({'success': 'Запись успешно удалена'})
        except PhoneRecord.DoesNotExist:
            return JsonResponse({'error': 'Запись не найдена'}, status=404)


# Список записей телефона по департаменту
class DepartmentPhoneRecordListView(ListView):
    model = PhoneRecord
    template_name = 'records/department_phone_record_list.html'
    context_object_name = 'phone_records'
    paginate_by = 25

    def get_queryset(self):
        department_id = self.kwargs.get('department_id')
        queryset = PhoneRecord.objects.filter(department_id=department_id)
        
        # Добавляем фильтрацию по параметрам поиска
        phone = self.request.GET.get('phone')
        port_asl = self.request.GET.get('port_asl')
        lin = self.request.GET.get('lin')
        if phone:
            queryset = queryset.filter(Q(phone_4__icontains=phone) | Q(phone_6__icontains=phone))
        if port_asl:
            queryset = queryset.filter(port_asl__icontains=port_asl)
        if lin:
            queryset = queryset.filter(lin__icontains=lin)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_id = self.kwargs.get('department_id')

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            department = None

        context['department'] = department
        context['can_edit'] = self.request.user.is_authenticated and (
            self.request.user.is_superuser or self.request.user.groups.filter(name="Механники тех учета").exists()
        )
        context['create_form'] = PhoneRecordForm()

        # Пагинация
        paginator = Paginator(self.object_list, 25)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            records = []
            for record in context['phone_records']:
                records.append({
                    'id': record.id,
                    'phone_4': record.phone_4,
                    'phone_6': record.phone_6,
                    'port_asl': record.port_asl,
                    'stan': record.stan,
                    'lin': record.lin,
                })
            return JsonResponse({'records': records})

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not (user.is_authenticated and (user.is_superuser or user.groups.filter(name="Механники тех учета").exists())):
            return JsonResponse({'error': 'Нет прав для создания записи.'}, status=403)

        form = PhoneRecordForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            # Привязываем запись к текущей организации
            department_id = self.kwargs.get('department_id')
            new_record.department_id = department_id
            new_record.save()
            return JsonResponse({'success': 'Запись успешно добавлена'})
        return JsonResponse({'error': 'Ошибка при добавлении записи'}, status=400)


# Список номеров населения (не привязанных к организации)
class PopulationPhoneRecordListView(ListView):
    model = PhoneRecord
    template_name = 'records/population_phone_record_list.html'
    context_object_name = 'phone_records'
    paginate_by = 25

    def get_queryset(self):
        return PhoneRecord.objects.filter(department__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Пагинация
        paginator = Paginator(self.object_list, 25)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


# Список повреждений
from django.db.models import Q

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

class DamageRecordListView(ListView):
    model = DamageRecord
    template_name = 'records/damage_record_list.html'
    context_object_name = 'damage_records'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтрация по телефону, если указано
        phone = self.request.GET.get('phone')
        if phone:
            queryset = queryset.filter(
                Q(phone_record__phone_4__icontains=phone) | Q(phone_record__phone_6__icontains=phone)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')  # Номер страницы
        paginator = Paginator(self.get_queryset(), self.paginate_by)  # Используем метод get_queryset() для пагинации
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['phone'] = self.request.GET.get('phone')  # Передаем параметр поиска телефона в шаблон

        return context


# Создание записи повреждения
class DamageRecordCreateView(TechMechanicRequiredMixin, CreateView):
    model = DamageRecord
    template_name = 'records/damage_record_form.html'
    fields = ['phone_record', 'comment', 'failure_type']
    success_url = reverse_lazy('damage-record-add')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['damages'] = DamageRecord.objects.all().order_by('-id')
        return context


# Список организаций
class OrganizationListView(ListView):
    model = Department
    template_name = 'records/organization_list.html'
    context_object_name = 'departments'


# Выход
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def custom_logout(request):
    logout(request)
    return redirect('/login/')
