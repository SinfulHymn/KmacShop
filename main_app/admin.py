from django.contrib import admin
from .models import Category, Product, ProductImage, Order, ProductReview

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
    list_display = ['name', 'description', 'price', 'in_stock', 'is_active', 'slug', 'created', 'updated']
    # filter is used to filter the products by category in the admin interface django-filter
    list_filter = ['in_stock', 'is_active']
    # editable is used to make the fields editable in the admin interface
    list_editable = ['price', 'in_stock', 'is_active']
    # prepopulated_fields is used to automatically fill in the slug field
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'url']
    list_filter = ['product']
    list_editable = ['url']
    prepopulated_fields = {'url': ('url',)}

admin.site.register(ProductReview)
admin.site.register(Order)