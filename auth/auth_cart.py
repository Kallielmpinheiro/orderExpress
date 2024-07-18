from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from bson import ObjectId
from classes.product import Product
from classes.cartOrder import Cart

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def viewCart():
    cart_items = Cart.getCartItems()
    return render_template('cart.html', cart_items=cart_items)
    # cart_items = Cart.getCartItems()
    # cart_items_serializable = [item.serialize() for item in cart_items]
    # return render_template('cart.html', cart_items=cart_items_serializable)

@cart_bp.route('/add_to_cart/<product_name>')
@login_required
def addCart(product_name):
    product = next((p for p in Product.getByProducts() if p.nome == product_name), None)
    if product:
        Cart.addCart(product)
        flash(f"Produto {product_name} adicionado ao carrinho!")
    else:
        flash(f"Produto {product_name} não encontrado.")
    return redirect(url_for('user.index'))

@cart_bp.route('/remove_from_cart/<product_name>')
@login_required
def remove_from_cart(product_name):
    Cart.removeCart(product_name)
    flash(f"Produto {product_name} removido do carrinho!")
    return redirect(url_for('cart.viewCart'))

@cart_bp.route('/clear_cart')
@login_required
def clear_cart():
    Cart.clearCart()
    flash("Carrinho esvaziado!")
    return redirect(url_for('cart.viewCart'))

@cart_bp.route('/checkout')
@login_required
def checkout():
    cart_items = Cart.getCartItems()
    if not cart_items:
        flash("Seu carrinho está vazio!")
        return redirect(url_for('cart.viewCart'))
    cart_items_serializable = [item.serialize() for item in cart_items]
    return render_template('checkout.html', cart_items=cart_items_serializable)
