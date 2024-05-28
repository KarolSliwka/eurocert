from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'date_added')
    search_fields = ('name', 'description', 'category')
    list_filter = ('category', 'date_added')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'quantity', 'category', 'image', 'visible')
        }),
        ('Dates', {
            'fields': ('date_added',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_added',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'visible')
    search_fields = ('name',)
    list_filter = ('visible',)
    fieldsets = (
        (None, {
            'fields': ('name', 'visible')
        }),
    )
