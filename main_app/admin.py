from django.contrib import admin
from .models import Category, Product

# Register your models here.
# @admin is used to register the models vs admin.site.register(Category)
@admin.register(Category)
# class defines the admin interface for the Category model
class CategoryAdmin(admin.ModelAdmin):
    # list_display is used to display the fields in the admin interface
    list_display = ['name', 'slug']
    # prepopulated_fields is used to automatically fill in the slug field
    prepopulated_fields = {'slug': ('name',)}

# register the Product model
@admin.register(Product)
# class defines the admin interface for the Product model
class ProductAdmin(admin.ModelAdmin):
    #  list_display is used to display the fields in the admin interface
    list_display = ['name', 'description', 'slug', 'price', 'in_stock', 'created', 'updated']
    # filter is used to filter the products by category in the admin interface django-filter
    list_filter = ['in_stock', 'is_active']
    # editable is used to make the fields editable in the admin interface
    list_editable = ['price', 'in_stock']
    # prepopulated_fields is used to automatically fill in the slug field
    prepopulated_fields = {'slug': ('name',)}