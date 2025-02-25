from django.contrib import admin
from .models import CustomUser, Activation


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'type_to_confirm', 'services_stopped', 'wallet', 'timezone')
    list_filter = ('type_to_confirm', 'services_stopped', 'timezone')
    search_fields = ('username', 'email')


@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'code', 'email', 'user_type', 'last_login_ip', 'mfa_token')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'email', 'code', 'last_login_ip', 'mfa_token')
