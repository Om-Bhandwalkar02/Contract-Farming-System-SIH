from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('contact', 'full_name', 'role', 'is_staff', 'is_superuser')
    search_fields = ('contact', 'full_name')
    ordering = ('contact',)
    readonly_fields = ('registration_date',)

    fieldsets = (
        (None, {'fields': ('contact', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'registration_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('contact', 'full_name', 'password1', 'password2', 'role'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
