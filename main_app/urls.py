from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # index page
    path('', views.index, name='index'),
    # product detail page
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    # category index page
    path('categories/<slug:category_slug>/', views.category_index, name='catergory_index'),
    # category product detail page
    path('categories/<slug:category_slug>/products/<slug:product_slug>/', views.category_products, name='category_products'),
    path('products/<int:product_id>/add_review/', views.add_review, name='add_review'),
]
