from pydantic import BaseModel, Field
import pymongo
from database.mongodb import db

class Pedido(BaseModel):
    id_pedido: int
    id_cliente: int
    produtos: list[str]
    total: float
    status: str = "Pendente"
    
    class Config:
        orm_mode = True
    
    @staticmethod
    def enteringMongo(pedido : "Pedido"):
        pedido_data = pedido.model_dump()
        result = db.pedidos.insert_one(pedido_data)
        print(f"Pedido {pedido.id_pedido} salvo no MongoDB com o ID: {result.inserted_id}")