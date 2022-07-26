from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from main_app.models import Product
from .cart import Cart
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/summary.html', {'cart': cart})

def cart_add(request):
    # print("test")
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        # same as 
        # product = Product.objects.get(id=product_id)
        # product is now a Product object ex. Product(id=1, name='product1', price=10)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product = product, quantity = product_qty)
        cartqty = cart.__len__()
        response = JsonResponse({'quantity': cartqty})
        return response