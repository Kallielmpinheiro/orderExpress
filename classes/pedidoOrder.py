import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pydantic import BaseModel, Field
from database.mongodb import db
from typing import List
from bson import ObjectId
from datetime import datetime
from flask_login import current_user    
import logging
from flask import jsonify, url_for

RECEIPT_DIR = 'receipts'
os.makedirs(RECEIPT_DIR, exist_ok=True)

class Pedido(BaseModel):
    cpf: str
    itens: List[dict]
    total_price: float
    status: str = Field(default="pendente")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: datetime = None

    def saveMongo(self):
        pedidos = db.pedidos
        pedido_dict = self.dict(by_alias=True)
        result = pedidos.insert_one(pedido_dict)
        pedido_dict["_id"] = str(result.inserted_id)
        return pedido_dict

    @staticmethod
    def updateStatus(pedido_id, status):
        pedidos = db.pedidos
        update_data = {"status": status}
        if status == "pago":
            update_data["paid_at"] = datetime.utcnow()
        result = pedidos.update_one({"_id": ObjectId(pedido_id)}, {"$set": update_data})
        return result.modified_count > 0

    @staticmethod
    def findById(pedido_id):
        pedidos = db.pedidos
        return pedidos.find_one({"_id": ObjectId(pedido_id)})

    @staticmethod
    def findByCpf(cpf):
        pedidos = db.pedidos
        return list(pedidos.find({"cpf": cpf}))

    @staticmethod
    def findAll():
        pedidos = db.pedidos
        return list(pedidos.find({}))

def generateReceipt(data, pedido_id):
    receipt_path = os.path.join(RECEIPT_DIR, f'recibo_{pedido_id}.pdf')
    p = canvas.Canvas(receipt_path, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Recibo de Pedido")
    p.drawString(100, 730, f"CPF: {data['cpf']}")
    p.drawString(100, 710, f"Data de Emissão: {data['created_at'].strftime('%d/%m/%Y %H:%M:%S')}")
    if data.get('paid_at'):
        p.drawString(100, 690, f"Data de Pagamento: {data['paid_at'].strftime('%d/%m/%Y %H:%M:%S')}")
    p.drawString(100, 670, "Itens:")

    y = 650
    for item in data['itens']:
        p.drawString(120, y, f"Nome: {item['nome']}, Descrição: {item['descricao']}, Preço: R$ {item['price']}")
        y -= 20

    p.drawString(100, y, f"Preço Total: R$ {data['total_price']}")

    p.showPage()
    p.save()

    return receipt_path

def historicoPedidos():
    try:
        cpf = current_user.cpf
        
        if not cpf:
            logging.error("CPF do usuário não encontrado")
            return jsonify({"error": "CPF do usuário não encontrado"}), 400

        logging.info(f"Consultando pedidos do CPF: {cpf}")

        pedidos = Pedido.findByCpf(cpf)
        if not pedidos:
            logging.info(f"Nenhum pedido encontrado para o CPF: {cpf}")
            return jsonify({"message": "Nenhum pedido encontrado"}), 404

        pedidos_list = []
        for pedido in pedidos:
            pedido['_id'] = str(pedido['_id'])
            pedidos_list.append(pedido)
            generateReceipt(pedido, pedido['_id'])

        return jsonify(pedidos_list), 200

    except Exception as e:
        logging.error(f"Erro ao consultar histórico de pedidos: {e}")
        return jsonify({"error": "Erro ao consultar histórico de pedidos"}), 500

def listarTodosPedidos():
    try:
        if not current_user.tipoUser == 'admin':
            logging.error("Acesso negado: usuário não é administrador")
            return jsonify({"error": "Acesso negado"}), 403

        logging.info("Consultando todos os pedidos")

        pedidos = Pedido.findAll()
        if not pedidos:
            logging.info("Nenhum pedido encontrado")
            return jsonify({"message": "Nenhum pedido encontrado"}), 404

        pedidos_list = []
        for pedido in pedidos:
            pedido['_id'] = str(pedido['_id'])
            pedidos_list.append(pedido)
            generateReceipt(pedido, pedido['_id'])

        return jsonify(pedidos_list), 200

    except Exception as e:
        logging.error(f"Erro ao consultar todos os pedidos: {e}")
        return jsonify({"error": "Erro ao consultar todos os pedidos"}), 500
