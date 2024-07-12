from pydantic import BaseModel
from database.mongodb import db

class Product(BaseModel):
    id_product: int
    nome: str
    descricao: str
    price: float

    class Config:
        orm_mode = True

    @staticmethod
    def save_to_mongo(product: 'Product'):
        product_data = product.model_dump()
        result = db.products.insert_one(product_data)
        print(f"Produto {product.id_product} salvo no MongoDB com o ID: {result.inserted_id}")
