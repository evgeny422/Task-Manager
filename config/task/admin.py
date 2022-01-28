from django.contrib import admin

from .models import Task


@admin.register(Task)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "url", "category", "user","is_active")
    list_display_links = ("url",)
    search_fields = ('url',)
    list_editable = ('is_active',)
    list_filter = ('category', 'status', 'created_at',)
