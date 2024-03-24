from django.contrib import admin
from apps.models import Users, Apartaments, Manager
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(Users)


class ApartamentsAdmin(admin.ModelAdmin):
    list_display = ('number', 'objects_ap', 'floor', 'ap', 'date_at', 'status_choices', 'price', 'client', 'info')
    list_filter = ('status_choices',)
    list_editable = ('client',)


admin.site.register(Apartaments, ApartamentsAdmin)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'count')
    fields = ['full_name', 'phone_number', 'email', 'password', 'count']

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(Manager, ManagerAdmin)
