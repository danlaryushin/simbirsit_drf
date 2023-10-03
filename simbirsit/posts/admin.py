from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput
from django.utils.safestring import mark_safe

from simbirsit.settings import EMPTY

from .models import Category, Post, Product, Sale


class DefaultAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 20})},
        models.DecimalField: {
            'widget': Textarea(attrs={'rows': 1, 'cols': 7})
        },
    }

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60'>")
        return None

    image_preview.__name__ = 'Фото'


@admin.register(Post)
class PostAdmin(DefaultAdmin):
    list_display = (
        'pub_date',
        'image_preview',
        'category',
        'sale',
    )
    list_editable = (
        'category',
        'sale',
    )
    list_filter = (
        'pub_date',
        'category',
    )
    empty_value_display = EMPTY


@admin.register(Category)
class CategoryAdmin(DefaultAdmin):
    list_display = (
        'title',
        'description',
    )
    empty_value_display = EMPTY


@admin.register(Product)
class ProductAdmin(DefaultAdmin):
    list_display = (
        'number',
        'image_preview',
        'title',
        'price',
        'is_active',
        'is_available',
        'owner',
    )
    ordering = ('-pub_date',)
    search_fields = ('number', 'title')
    list_editable = ('is_active', 'price')
    list_filter = (
        'pub_date',
        'category',
        'is_available',
        'is_active',
    )
    empty_value_display = EMPTY


class SaleInline(admin.TabularInline):
    model = Product
    readonly_fields = ('image_preview',)
    ordering = ('pub_date',)
    extra = 0
    show_change_link = True
    exclude = ('owner', 'is_available', 'category')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 20})},
        models.DecimalField: {
            'widget': Textarea(attrs={'rows': 1, 'cols': 7})
        },
    }

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60'>")
        return None

    image_preview.__name__ = 'Фото'


@admin.register(Sale)
class SaleAdmin(DefaultAdmin):
    list_display = ('date',)
    empty_value_display = EMPTY
    inlines = [SaleInline]
