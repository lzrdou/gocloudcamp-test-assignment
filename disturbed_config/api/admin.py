from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from reversion.admin import VersionAdmin
from .models import Service, Config, ServiceConfig


class ServiceConfigInlineFormset(BaseInlineFormSet):
    def clean_service(self):
        if len(self.cleaned_data['service']) < 1:
            return 'Необходимо добавить сервис'
        return self.cleaned_data['service']


class ServiceConfigInline(admin.TabularInline):
    model = ServiceConfig
    formset = ServiceConfigInlineFormset
    min_num = 1
    max_num = 1
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
        'slug'
    )


@admin.register(Config)
class ConfigAdmin(VersionAdmin):
    list_display = (
        'name',
    )
    list_filter = (
        'service',
        'status'
    )
    search_fields = (
        'name',
        'service'
    )
    inlines = (ServiceConfigInline,)


@admin.register(ServiceConfig)
class ServiceConfigAdmin(admin.ModelAdmin):
    list_display = (
        'service',
        'config'
    )
    list_filter = (
        'service',
        'config'
    )
    search_fields = (
        'service',
        'config'
    )
