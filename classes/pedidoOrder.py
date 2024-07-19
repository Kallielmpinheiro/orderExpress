from pydantic import BaseModel, Field
from database.mongodb import db
from typing import List

class Pedido(BaseModel):
    cpf: str
    itens: List[dict]
    total_price: float
    
    def saveMongo(self):
        pedidos = db.pedidos
        pedido_dict = self.dict(by_alias=True)
        result = pedidos.insert_one(pedido_dict)
        pedido_dict["_id"] = str(result.inserted_id)
        return pedido_dict
