from django.contrib import admin
from .models import Category, Service, Feedback, Item

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'updated']
    list_filter = ['created', 'updated']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'created', 'updated']
    list_filter = ['created', 'updated']
    list_editable = ['price']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['name', 'created']

