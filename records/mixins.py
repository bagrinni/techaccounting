from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden

class TechMechanicRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Миксин, разрешающий доступ только пользователям, входящим в группу "Механники тех учета"
    или суперпользователям.
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Механники тех учета").exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        return HttpResponseForbidden("У вас нет доступа к этому разделу.")
