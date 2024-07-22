from flask import session, render_template

class Cart:
    @staticmethod
    def inicializarCarrinho():
        if 'cart' not in session:
            session['cart'] = []

    @staticmethod
    def adicionarItem(produto):
        Cart.inicializarCarrinho()
        session['cart'].append(produto.dict())
        session.modified = True

    @staticmethod
    def removerItem(nomeProduto):
        Cart.inicializarCarrinho()
        session['cart'] = [item for item in session['cart'] if item['nome'] != nomeProduto]
        session.modified = True

    @staticmethod
    def obterItens():
        Cart.inicializarCarrinho()
        return session['cart']

    @staticmethod
    def limpar():
        session.pop('cart', None)
        session.modified = True

    @staticmethod
    def renderizarCarrinho():
        cart_items = Cart.obterItens()
        total_price = sum(item['price'] for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)