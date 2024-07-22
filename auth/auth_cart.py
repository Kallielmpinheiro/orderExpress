from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
from classes.product import Product
from classes.cartOrder import Cart

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/carrinho')
@login_required
def exibirCarrinho():
    return Cart.renderizarCarrinho()

@cart_bp.route('/adicionar_ao_carrinho/<product_name>')
@login_required
def adicionarAoCarrinho(product_name):
    product = next((p for p in Product.getByProducts() if p.nome == product_name), None)
    if product:
        Cart.adicionarItem(product)
        flash(f"Produto {product_name} adicionado ao carrinho!")
    else:
        flash(f"Produto {product_name} não encontrado.")
    return redirect(url_for('user.index'))

@cart_bp.route('/remover_do_carrinho/<product_name>')
@login_required
def removerDoCarrinho(product_name):
    Cart.removerItem(product_name)
    flash(f"Produto {product_name} removido do carrinho!")
    return redirect(url_for('cart.exibirCarrinho'))

@cart_bp.route('/limpar_carrinho')
@login_required
def limparCarrinho():
    Cart.limpar()
    flash("Carrinho esvaziado!")
    return redirect(url_for('cart.exibirCarrinho'))
