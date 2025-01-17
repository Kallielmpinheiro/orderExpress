import os
from flask import Blueprint, request, redirect, url_for, flash, jsonify, send_from_directory, render_template
from flask_login import login_required, current_user
from classes.pedidoOrder import Pedido, generateReceipt, historicoPedidos, listarTodosPedidos
from classes.cartOrder import Cart
import logging
import json
import stripe
from dotenv import load_dotenv

pedidos_bp = Blueprint('pedidos', __name__)

load_dotenv()
stripe.api_key = os.getenv('STRIPE_API_KEY')

@pedidos_bp.route('/place_order', methods=['POST'])
@login_required
def placeOrder():

    data = request.form.to_dict()
    try:
        data['itens'] = json.loads(data['itens'])
    except json.JSONDecodeError as e:
        flash("Erro ao decodificar itens do pedido.")
        return redirect(url_for('cart.exibirCarrinho'))

    total_price = sum(item['price'] for item in data['itens'])
    data['total_price'] = total_price

    coupon_code = data.get('coupon_code', None)
    discounts = []

    if coupon_code:
        try:
            coupon = stripe.Coupon.retrieve(coupon_code)
            if coupon and coupon.valid:
                discounts.append({'coupon': coupon.id})
                flash(f"Cupom aplicado: {coupon.id}")
            else:
                flash("Cupom inválido ou expirado.")
        except Exception as e:
            flash(f"Erro ao aplicar cupom: {str(e)}")

    try:
        pedido = Pedido(**data)
        pedido_data = pedido.saveMongo()
        flash("Pedido realizado com sucesso! Aguardando pagamento.")        
        Cart.limpar()

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
            discounts=discounts,
            success_url=url_for('pedidos.payment_success', pedido_id=pedido_data["_id"], _external=True),
            cancel_url=url_for('cart.exibirCarrinho', _external=True),
        )

        return redirect(session.url, code=303)

    except Exception as e:
        flash(f"Erro ao realizar o pedido: {str(e)}")
        return redirect(url_for('cart.exibirCarrinho'))

@pedidos_bp.route('/payment_success/<pedido_id>')
@login_required
def payment_success(pedido_id):
    try:
            if Pedido.updateStatus(pedido_id, "pago"):
                flash("Pagamento realizado com sucesso! Pedido atualizado para 'pago'.")
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

@pedidos_bp.route('/cupom', methods=['POST'])
@login_required
def criarCupom():
    if current_user.tipoUser != 'admin':
        flash("Acesso negado: usuário não é administrador")
        return redirect(url_for('user.index'))
    
    data = request.form.to_dict()
    try:
        percent_off = float(data.get('percent_off', 0))
        coupon = stripe.Coupon.create(
            percent_off=int(percent_off),
            duration='once'
        )
        flash(f"Cupom criado com sucesso: {coupon.id}")
        logging.info(f"Cupom criado com sucesso: {coupon.id}")
        return redirect(url_for('user.indexadmin'))

    except ValueError as e:
        flash("Valor de desconto inválido.")
        logging.error(f"Valor de desconto inválido: {e}")
        return redirect(url_for('user.indexadmin'))
    except Exception as e:
        flash(f"Erro ao criar cupom: {str(e)}")
        logging.error(f"Erro ao criar cupom: {e}")
        return redirect(url_for('user.indexadmin'))

@pedidos_bp.route('/admin/revoke_coupon', methods=['POST'])
@login_required
def revogarCupom():
    if current_user.tipoUser != 'admin':
        flash("Acesso negado: usuário não é administrador")
        return redirect(url_for('user.index'))

    data = request.form.to_dict()
    coupon_id = data.get('coupon_id')

    try:
        coupon = stripe.Coupon.modify(
            coupon_id,
            valid=False
        )
        flash(f"Cupom revogado com sucesso: {coupon.id}")
        logging.info(f"Cupom revogado com sucesso: {coupon.id}")
        return redirect(url_for('user.indexadmin'))

    except Exception as e:
        flash(f"Erro ao revogar cupom: {str(e)}")
        logging.error(f"Erro ao revogar cupom: {e}")
        return redirect(url_for('user.indexadmin'))

@pedidos_bp.route('/retry_payment/<pedido_id>')
@login_required
def retry_payment(pedido_id):
    try:
        pedido = Pedido.findById(pedido_id)
        if not pedido:
            flash("Pedido não encontrado.")
            return redirect(url_for('pedidos.retornarhistorico'))

        if pedido['status'] == 'pago':
            flash("Este pedido já foi pago.")
            return redirect(url_for('pedidos.retornarhistorico'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': 'Pedido ' + str(pedido["_id"]),
                    },
                    'unit_amount': int(pedido['total_price'] * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('pedidos.payment_success', pedido_id=pedido["_id"], _external=True),
            cancel_url=url_for('pedidos.retornarhistorico', _external=True),
        )

        return redirect(session.url, code=303)

    except Exception as e:
        logging.error(f"Erro ao tentar pagamento novamente: {e}")
        flash(f"Erro ao tentar pagamento novamente: {str(e)}")
        return redirect(url_for('pedidos.retornarhistorico'))
