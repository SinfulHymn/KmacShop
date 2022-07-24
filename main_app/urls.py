from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/<slug:category_slug>/', views.category_index, name='catergory_index'),
]
