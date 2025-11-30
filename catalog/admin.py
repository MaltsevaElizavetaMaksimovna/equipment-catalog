from django.contrib import admin
from .models import (Workshop, Site, EquipmentType, Equipment, 
                     EquipmentCharacteristic, EquipmentDocument)


class SiteInline(admin.TabularInline):
    model = Site
    extra = 1


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description']
    search_fields = ['name', 'code']
    inlines = [SiteInline]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'workshop']
    list_filter = ['workshop']
    search_fields = ['name']


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class CharacteristicInline(admin.TabularInline):
    model = EquipmentCharacteristic
    extra = 2


class DocumentInline(admin.TabularInline):
    model = EquipmentDocument
    extra = 1


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['inventory_number', 'name', 'equipment_type', 'site', 
                    'manufacturer', 'status', 'year']
    list_filter = ['equipment_type', 'status', 'site__workshop']
    search_fields = ['name', 'inventory_number', 'manufacturer', 'model', 'serial_number']
    inlines = [CharacteristicInline, DocumentInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'inventory_number', 'equipment_type', 'site', 'status')
        }),
        ('Технические данные', {
            'fields': ('manufacturer', 'model', 'serial_number', 'year')
        }),
        ('Дополнительно', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(EquipmentCharacteristic)
class EquipmentCharacteristicAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'name', 'value', 'unit']
    list_filter = ['equipment__equipment_type']
    search_fields = ['name', 'value']


@admin.register(EquipmentDocument)
class EquipmentDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'equipment', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['title', 'equipment__name']
