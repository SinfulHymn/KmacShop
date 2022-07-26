

from math import prod


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
        
        
    def __len__(self):
        # get cart data and count the number of items
        return sum(item["quantity"] for item in self.cart.values())