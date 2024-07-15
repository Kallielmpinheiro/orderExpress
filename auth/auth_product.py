from flask import Blueprint, render_template, request, redirect, url_for, flash
from classes.product import Product
from database.mongodb import db, client

product_bp = Blueprint('product', __name__)

@product_bp.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        id_product = int(request.form['id_product'])
        nome = request.form['nome']
        descricao = request.form['descricao']
        price = float(request.form['price'])

        product = Product(
            id_product=id_product,
            nome=nome,
            descricao=descricao,
            price=price
        )
        try:
            Product.saveToMongo(product)
            flash(f'Produto {nome} criado com sucesso!')
        except Exception as e:
            flash(f'Erro ao criar produto: {e}')
        
        return redirect(url_for('product.create_product'))
    
    return render_template('admin.html')

@product_bp.route('/edit_product', methods=['POST'])
def edit_product():
    id_product = int(request.form['id_product_edit'])
    nome = request.form['nome_edit']
    descricao = request.form['descricao_edit']
    price = float(request.form['price_edit'])

    try:
        Product.editarProduto(id_product, nome, descricao, price)
        flash(f'Produto {id_product} atualizado com sucesso!')
    except Exception as e:
        flash(f'Erro ao atualizar produto: {e}')
    
    return redirect(url_for('product.create_product'))

@product_bp.route('/delete_product', methods=['POST'])
def delete_product():
    id_product = int(request.form['id_product_delete'])
    try:
        Product.excluirProduto(id_product)
        flash(f'Produto {id_product} excluído com sucesso!')
    except Exception as e:
        flash(f'Erro ao excluir produto: {e}')
    
    return redirect(url_for('product.create_product'))