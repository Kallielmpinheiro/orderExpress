from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
from database.mongodb import db

class Product(BaseModel):
    nome: str
    descricao: str
    price: float
    id: str = Field(default_factory=lambda: str(ObjectId()), alias='_id')

    class Config:
        orm_mode = True

    @classmethod
    def saveToMongo(cls, product: 'Product'):
        product_data = product.model_dump(by_alias=True, exclude_unset=True)
        result = db.products.insert_one(product_data)
        print(f"Produto {product.nome} salvo no MongoDB com o ID: {result.inserted_id}")
        return result.inserted_id

    @classmethod
    def editarProduto(cls, nome: str, descricao: str, price: float):
        result = db.products.update_one(
            {"nome": nome},
            {"$set": {"descricao": descricao, "price": price}}
        )
        if result.modified_count > 0:
            print(f"Produto {nome} atualizado com sucesso!")
        else:
            print(f"Produto {nome} não encontrado ou nenhuma alteração foi feita.")

    @classmethod
    def excluirProduto(cls, nome: str):
        result = db.products.delete_one({"nome": nome})
        if result.deleted_count > 0:
            print(f"Produto {nome} excluído com sucesso!")
        else:
            print(f"Produto {nome} não encontrado.")

    @classmethod
    def getByProducts(cls) -> List['Product']:
        products = db.products.find()
        return [cls(**cls.__adapt_document(product)) for product in products]

    @staticmethod
    def __adapt_document(product_doc: dict) -> dict:
        product_doc['_id'] = str(product_doc['_id'])
        return product_doc
