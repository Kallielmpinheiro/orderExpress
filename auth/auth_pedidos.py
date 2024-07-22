import os
from flask import Blueprint, request, redirect, url_for, flash, jsonify, send_file, render_template, send_from_directory
from flask_login import login_required, current_user
from classes.pedidoOrder import Pedido, generateReceipt, historicoPedidos, listarTodosPedidos
from classes.cartOrder import Cart
import logging
import json
import stripe

pedidos_bp = Blueprint('pedidos', __name__)

logging.basicConfig(level=logging.INFO)

stripe.api_key = ''

@pedidos_bp.route('/place_order', methods=['POST'])
@login_required
def placeOrder():
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
        flash("Pedido realizado com sucesso! Aguardando pagamento.")
        logging.info(f"Pedido salvo no MongoDB: {pedido_data}")
        
        Cart.clearCart()

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': 'Pedido ' + str(pedido_data["_id"]),
                    },
                    'unit_amount': int(total_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('pedidos.payment_success', pedido_id=pedido_data["_id"], _external=True),
            cancel_url=url_for('cart.viewCart', _external=True),
        )

        return redirect(session.url, code=303)

    except Exception as e:
        flash(f"Erro ao realizar o pedido: {str(e)}")
        logging.error(f"Erro ao processar o pedido: {e}")
        return redirect(url_for('cart.viewCart'))

@pedidos_bp.route('/payment_success/<pedido_id>')
@login_required
def payment_success(pedido_id):
    try:
        if Pedido.updateStatus(pedido_id, "pago"):
            flash("Pagamento realizado com sucesso! Pedido atualizado para 'pago'.")
            logging.info(f"Pedido {pedido_id} atualizado para 'pago'.")

            pedido_data = Pedido.findById(pedido_id)

            if pedido_data:
                receipt_path = generateReceipt(pedido_data, pedido_id)
                receipt_url = url_for('pedidos.download_receipt', filename=os.path.basename(receipt_path))

                return render_template('payment_success.html', receipt_url=receipt_url, index_url=url_for('user.index'))

            flash("Erro ao gerar o recibo.")
            return redirect(url_for('user.index'))

        flash("Erro ao atualizar o status do pedido.")
        return redirect(url_for('user.index'))

    except Exception as e:
        flash(f"Erro ao processar o pagamento: {str(e)}")
        logging.error(f"Erro ao processar o pagamento: {e}")
        return redirect(url_for('user.index'))

@pedidos_bp.route('/receipts/<filename>')
@login_required
def download_receipt(filename):
    return send_from_directory('receipts', filename, as_attachment=True)

@pedidos_bp.route('/order/<order_id>')
@login_required
def view_order(order_id):
    order = Pedido.findById(order_id)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({"error": "Pedido não encontrado"}), 404

@pedidos_bp.route('/history')
@login_required
def retornarhistorico():
    return historicoPedidos()

@pedidos_bp.route('/listarTodosPedidos', methods=['GET'])
@login_required
def listar_todos_pedidos():
    return listarTodosPedidos()
