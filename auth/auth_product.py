import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from classes.product import Product
from decorators import admin_required
from security.forms import LoginForm, RegisterForm, SuspendUserForm, UnsuspendUserForm, ProductForm
from flask_login import login_required
from decorators import csrf
from bson import ObjectId
import logging

from database.mongodb import db

product_bp = Blueprint('product', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@product_bp.route('/create_product', methods=['GET', 'POST'])
@admin_required
@login_required
@csrf.exempt
def createProduct():
    form_product = ProductForm()
    form_suspend = SuspendUserForm()
    form_unsuspend = UnsuspendUserForm()
    
    if form_product.validate_on_submit():
        nome = form_product.nome.data
        descricao = form_product.descricao.data
        price = float(form_product.price.data)
        
        product = Product(
            nome=nome,
            descricao=descricao,
            price=price
        )
        try:
            product.createInMongo()
            flash(f'Produto {nome} criado com sucesso!')
        except Exception as e:
            flash(f'Erro ao criar produto: {e}')
        
        return redirect(url_for('product.createProduct'))
    
    return render_template('admin.html', user_type='admin', form_product=form_product, form_suspend=form_suspend, form_unsuspend=form_unsuspend)

@product_bp.route('/edit_product', methods=['POST'])
@admin_required
@login_required
@csrf.exempt
def editProduct():
    try:
       
        product_id = request.form.get('product_id')
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        price = request.form.get('price')
        
        
        price = float(price)
        
       
        product = Product.getById(product_id)
        if not product:
            logging.error('Product not found.')
            flash('Produto não encontrado.')
            return redirect(url_for('user.index'))  
        
    
        product.nome = nome
        product.descricao = descricao
        product.price = price
        
        
        product.updateInMongo()
        
        logging.debug(f'Product {nome} updated successfully.')
        flash(f'Produto {nome} atualizado com sucesso!')
    except ValueError:
        logging.error('Invalid price provided.')
        flash('O preço fornecido é inválido.')
    except Exception as e:
        logging.error(f'Error updating product: {e}')
        flash(f'Erro ao atualizar produto: {e}')

    return redirect(url_for('user.index'))

@product_bp.route('/delete_product', methods=['POST'])
@admin_required
@login_required
def deleteProduct():
    product_id = request.form.get('product_id')
    if not product_id:
        logger.error('ID do produto não fornecido.')
        flash('ID do produto não fornecido', 'error')
        return redirect(url_for('user.index'))

    try:
        logger.debug(f'Attempting to delete product with ID: {product_id}')
        result = db.products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count > 0:
            logger.info(f'Product with ID {product_id} deleted successfully.')
            flash('Produto excluído com sucesso', 'success')
        else:
            logger.warning(f'Product with ID {product_id} not found.')
            flash('Produto não encontrado', 'error')
    except Exception as e:
        logger.error(f'Error deleting product with ID {product_id}: {e}')
        flash(f'Erro ao excluir produto: {e}', 'error')
    
    return redirect(url_for('user.index'))