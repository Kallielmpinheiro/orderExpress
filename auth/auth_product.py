from flask import Blueprint, render_template, request, redirect, url_for, flash
from classes.product import Product
from decorators import admin_required
from flask_login import login_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/create_product', methods=['GET', 'POST'])
@admin_required
@login_required
def createProduct():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        price = float(request.form['price'])

        product = Product(
            nome=nome,
            descricao=descricao,
            price=price
        )
        try:
            Product.saveToMongo(product)
            flash(f'Produto {nome} criado com sucesso!')
        except Exception as e:
            flash(f'Erro ao criar produto: {e}')
        
        return redirect(url_for('product.createProduct'))
    
    return render_template('admin.html')

@product_bp.route('/edit_product', methods=['POST'])
@admin_required
@login_required
def editProduct():
    nome = request.form['nome_edit']
    descricao = request.form['descricao_edit']
    price = float(request.form['price_edit'])

    try:
        Product.editarProduto(nome, descricao, price)
        flash(f'Produto {nome} atualizado com sucesso!')
    except Exception as e:
        flash(f'Erro ao atualizar produto: {e}')
    
    return redirect(url_for('product.createProduct'))

@product_bp.route('/delete_product', methods=['POST'])
@admin_required
@login_required
def deleteProduct():
    nome = request.form['nome']
    try:
        Product.excluirProduto(nome)
        flash(f'Produto {nome} excluído com sucesso!')
    except Exception as e:
        flash(f'Erro ao excluir produto: {e}')
    
    return redirect(url_for('product.createProduct'))
