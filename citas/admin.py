from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import ValidationError
from .models import Mascota, Cita


class SuperuserAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_superuser:
            raise ValidationError(
                "Solo el administrador principal puede acceder.",
                code='not_superuser',
            )


class SuperuserAdminSite(admin.AdminSite):
    login_form = SuperuserAuthenticationForm

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


admin_site = SuperuserAdminSite(name='admin')


@admin.register(Mascota, site=admin_site)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'nombre_dueno', 'telefono_dueno')
    search_fields = ('nombre', 'nombre_dueno', 'raza')
    list_filter = ('especie',)

@admin.register(Cita, site=admin_site)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'fecha', 'hora', 'motivo', 'estado')
    list_filter = ('fecha', 'estado')
    search_fields = ('mascota__nombre', 'mascota__nombre_dueno', 'motivo')
    date_hierarchy = 'fecha'
    list_editable = ('estado',)
