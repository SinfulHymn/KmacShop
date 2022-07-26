from urllib import response
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
        # print(product.name ,'into add to cart')
        cart.add(product = product, quantity = product_qty)
        # print(cart)
        cartqty = cart.__len__()
        # print('cartqty:~',cartqty)
        response = JsonResponse({'quantity': cartqty})
        return response
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'delete':
        product_id = request.POST.get('productid')
        print('product_id:~',product_id)
        cart.delete(product=product_id)
        response = JsonResponse({'success': True})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'update':
        product_id = request.POST.get('productid')
        product_qty = request.POST.get('productqty')
        print('product_id:~',product_id, type(product_id))
        print('product_qty:~',product_qty, type(product_qty))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'success': True})
        return response