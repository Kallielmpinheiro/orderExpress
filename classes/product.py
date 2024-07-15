from pydantic import BaseModel
from database.mongodb import db, client

class Product(BaseModel):
    id_product: int
    nome: str
    descricao: str
    price: float

    class Config:
        orm_mode = True


    def getByIdProducts():
        pass

    @staticmethod
    def saveToMongo(product: 'Product'):
        product_data = product.model_dump()
        result = db.products.insert_one(product_data)
        print(f"Produto {product.id_product} salvo no MongoDB com o ID: {result.inserted_id}")
        
    @staticmethod
    def editarProduto(id_product: int, nome: str, descricao: str, price: float):
        result = db.products.update_one(
            {"id_product": id_product},
            {"$set": {"nome": nome, "descricao": descricao, "price": price}}
        )
        if result.modified_count > 0:
            print(f"Produto {id_product} atualizado com sucesso!")
        else:
            print(f"Produto {id_product} não encontrado ou nenhuma alteração foi feita.")

    @staticmethod
    def excluirProduto(id_product: int):
        result = db.products.delete_one({"id_product": id_product})
        if result.deleted_count > 0:
            print(f"Produto {id_product} excluído com sucesso!")
        else:
            print(f"Produto {id_product} não encontrado.")