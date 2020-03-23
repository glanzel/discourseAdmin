from django.contrib import admin
from .models import Bread, Cake
from django_baker.admin import ExtendedModelAdminMixin


class BreadAdmin(ExtendedModelAdminMixin, admin.ModelAdmin):
    extra_list_display = []
    extra_list_filter = []
    extra_search_fields = []
    list_editable = []
    raw_id_fields = []
    inlines = []
    filter_vertical = []
    filter_horizontal = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = []


class CakeAdmin(ExtendedModelAdminMixin, admin.ModelAdmin):
    extra_list_display = []
    extra_list_filter = []
    extra_search_fields = []
    list_editable = []
    raw_id_fields = []
    inlines = []
    filter_vertical = []
    filter_horizontal = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = []


admin.site.register(Bread, BreadAdmin)
admin.site.register(Cake, CakeAdmin)
