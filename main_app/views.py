from django.shortcuts import render, get_object_or_404
from .models import Category, Product
# Create your views here.



def index(request):
    products = Product.products.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})

def category_index(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category= category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})

def category_products(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)
    return render(request, 'store/products/detail.html', {'product': product})

def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('main_app:product_detail', product_slug)
    else:
        form = ReviewForm()
    return render(request, 'store/products/add_review.html', {'product': product, 'form': form})