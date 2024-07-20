import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pydantic import BaseModel, Field
from database.mongodb import db
from typing import List
from bson import ObjectId

RECEIPT_DIR = 'receipts'
os.makedirs(RECEIPT_DIR, exist_ok=True)

class Pedido(BaseModel):
    cpf: str
    itens: List[dict]
    total_price: float
    status: str = Field(default="pendente")

    def save_mongo(self):
        pedidos = db.pedidos
        pedido_dict = self.dict(by_alias=True)
        result = pedidos.insert_one(pedido_dict)
        pedido_dict["_id"] = str(result.inserted_id)
        return pedido_dict

    @staticmethod
    def update_status(pedido_id, status):
        pedidos = db.pedidos
        result = pedidos.update_one({"_id": ObjectId(pedido_id)}, {"$set": {"status": status}})
        return result.modified_count > 0

    @staticmethod
    def find_by_id(pedido_id):
        pedidos = db.pedidos
        return pedidos.find_one({"_id": ObjectId(pedido_id)})

def generate_receipt(data, pedido_id):
    receipt_path = os.path.join(RECEIPT_DIR, f'recibo_{pedido_id}.pdf')
    p = canvas.Canvas(receipt_path, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Recibo de Pedido")
    p.drawString(100, 730, f"CPF: {data['cpf']}")
    p.drawString(100, 710, "Itens:")

    y = 690
    for item in data['itens']:
        p.drawString(120, y, f"Nome: {item['nome']}, Descrição: {item['descricao']}, Preço: R$ {item['price']}")
        y -= 20

    p.drawString(100, y, f"Preço Total: R$ {data['total_price']}")

    p.showPage()
    p.save()

    return receipt_path