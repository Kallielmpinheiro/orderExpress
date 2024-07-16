from pydantic import BaseModel
from database.mongodb import db, client

class Product(BaseModel):
    nome: str
    descricao: str
    price: float

    class Config:
        orm_mode = True

    @staticmethod
    def saveToMongo(product: 'Product'):
        product_data = product.model_dump()
        result = db.products.insert_one(product_data)
        print(f"Produto {product.nome} salvo no MongoDB com o ID: {result.inserted_id}")
        
    @staticmethod
    def editarProduto(nome: str, descricao: str, price: float):
        result = db.products.update_one(
            {"nome": nome},
            {"$set": {"descricao": descricao, "price": price}}
        )
        if result.modified_count > 0:
            print(f"Produto {nome} atualizado com sucesso!")
        else:
            print(f"Produto {nome} não encontrado ou nenhuma alteração foi feita.")

    @staticmethod
    def excluirProduto(nome: str):
        result = db.products.delete_one({"nome": nome})
        if result.deleted_count > 0:
            print(f"Produto {nome} excluído com sucesso!")
        else:
            print(f"Produto {nome} não encontrado.")
