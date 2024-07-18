from flask import session

class Cart:
    @staticmethod
    def initializeCart():
        if 'cart' not in session:
            session['cart'] = []

    @staticmethod
    def addCart(product):
        Cart.initializeCart()
        session['cart'].append(product.dict())
        session.modified = True

    @staticmethod
    def removeCart(product_name):
        Cart.initializeCart()
        session['cart'] = [item for item in session['cart'] if item['nome'] != product_name]
        session.modified = True

    @staticmethod
    def getCartItems():
        Cart.initializeCart()
        return session['cart']

    @staticmethod
    def clearCart():
        session.pop('cart', None)
