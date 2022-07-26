from math import prod
from main_app.models import Product
from decimal import Decimal

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
        product_id= str(product.id)
        # product_id = str(product.id)
        print('product_id:~',product_id, type(product_id))
        print('quantity:~',quantity, type(quantity))
        print('self.cart:~',self.cart, )
        
        if product_id not in self.cart:
            self.cart[str(product_id)] = {'price': str(product.price),'quantity': int(quantity)}
            print("!!!@@@@@@!!!",self.cart[f'{product_id}']['quantity'])
        else:
            print('its in!!!!$@#$@#$')
            self.cart[product_id]['quantity'] += int(quantity)
            self.session.modified = True
        
        self.session.modified = True
        print('self.cart:~',self.cart)
        print('self.session:~',self.session.get('cartsession'))
        print('self.cart.keys():~',self.cart.keys())
        print('self.cart.values():~',self.cart.values())
    
    
    def __iter__(self):
        # get the product id and quantity in the session cart to query the database for the products
        product_ids = self.cart.keys()
        print('product_ids:~',product_ids)
        products = Product.products.filter(id__in=product_ids)
        print(products)
        cart = self.cart.copy()
        
        for product in products:
            print('in for', product)
            cart[str(product.id)]['product'] = product
            
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        
    def __len__(self):
        # get cart data and count the number of items
        return sum(item["quantity"] for item in self.cart.values())
    
    def __str__(self):
        return str(self.cart)
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_order_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())+Decimal(10)