from django.contrib import admin

# Register your models here.
from user.models import RegisterUser


class RegisterUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'country',
        'profile_image', 'is_superuser', 'last_login')


admin.site.register(RegisterUser, RegisterUserAdmin)
