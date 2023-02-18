from django.contrib import admin
from .models import (Category, Product, ProductStock, Slider)


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}

admin.site.register([ProductStock, Slider])