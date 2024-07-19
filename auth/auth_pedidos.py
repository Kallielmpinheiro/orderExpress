from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from classes.pedidoOrder import Pedido
from database.mongodb import db
from bson import ObjectId
import logging
import json
from classes.cartOrder import Cart

pedidos_bp = Blueprint('pedidos', __name__)

logging.basicConfig(level=logging.INFO)

@pedidos_bp.route('/place_order', methods=['POST'])
@login_required
def place_order():
    logging.info("Iniciando o processamento do pedido")

    data = request.form.to_dict()
    logging.info(f"Dados do pedido recebidos como formulário: {data}")
    try:
        data['itens'] = json.loads(data['itens'])
        logging.info(f"Dados dos itens após conversão: {data['itens']}")
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar JSON: {str(e)}")
        flash(f"Erro ao decodificar itens do pedido.")
        return redirect(url_for('cart.viewCart'))

    total_price = sum(item['price'] for item in data['itens'])
    data['total_price'] = total_price

    try:
        pedido = Pedido(**data)
        pedido_data = pedido.saveMongo()
        flash("Pedido realizado com sucesso!")
        logging.info(f"Pedido salvo no MongoDB: {pedido_data}")
        Cart.clearCart()
        return redirect(url_for('cart.viewCart'))
    except Exception as e:
        flash(f"Erro ao realizar o pedido: {str(e)}")
        logging.error(f"Erro ao processar o pedido: {e}")
        return redirect(url_for('cart.viewCart'))

@pedidos_bp.route('/order/<order_id>')
@login_required
def view_order(order_id):
    pedidos = db.pedidos
    order = pedidos.find_one({"_id": ObjectId(order_id)})
    if order:
        return jsonify(order), 200
    else:
        return jsonify({"error": "Pedido não encontrado"}), 404
