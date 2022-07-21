from django.shortcuts import render
from .models import Category, Product
# Create your views here.
def index(request):
    products = Product.objects.all()
    
    
    return render(request, 'index.html', {'products': products})