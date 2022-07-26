from math import prod
from main_app.models import Product


class Cart():
    
    def __init__(self, request):
        self.session = request.session
        # print('~~~~',self.session)
        cart = self.session.get('cartsession')
        # print('cart:~',cart)
        if 'cartsession' not in request.session:
            # create a new cart session key
            cart = self.session['cartsession'] = {}
            
        # set the cart to the cart session key
        self.cart = cart
        
        
    def add(self, product, quantity):
        product_id = product.id
        
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price),'quantity': int(quantity)}
        
        self.session.modified = True
    
    
    def __iter__(self):
        # get the product id and quantity in the session cart to query the database for the products
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()
        
    def __len__(self):
        # get cart data and count the number of items
        return sum(item["quantity"] for item in self.cart.values())