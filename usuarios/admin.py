from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    # Campos que aparecem no admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Informações importantes', {'fields': ('perfil',)}),  # Adiciona o campo perfil
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos exibidos na lista de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'perfil', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'perfil')

    # Campos usados para criar um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'perfil', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(Usuario, UsuarioAdmin)
