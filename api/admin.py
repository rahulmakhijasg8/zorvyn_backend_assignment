from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Transaction


class CustomAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_staff
            and (request.user.is_superuser or request.user.role == 'Admin')
        )

admin_site = CustomAdminSite(name='admin')


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'isactive']
    list_filter = ['role', 'isactive']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'isactive')}),
    )
    

admin_site.register(User)
admin_site.register(Transaction)
