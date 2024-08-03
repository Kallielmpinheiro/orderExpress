import logging
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional
from database.mongodb import db

class Avaliacao(BaseModel):
    user_id: str
    estrelas_user: int = Field(..., ge=1, le=5, description="Número de estrelas da avaliação (1-5)")
    comentario_user: str = Field(..., min_length=1, description="Comentário do usuário")
    
    class Config:
        orm_mode = True

class Product(BaseModel):
    nome: str
    descricao: str
    price: float
    id: str = Field(default_factory=lambda: str(ObjectId()), alias='_id')
    avaliacoes: Optional[List[Avaliacao]] = []
    already_reviewed: Optional[bool] = False

    class Config:
        orm_mode = True

    def createInMongo(self):
        """ Cria um novo produto no MongoDB """
        try:
            product_data = self.dict(by_alias=True, exclude_unset=True)
            db.products.insert_one(product_data)
            logging.debug(f'Product {self.nome} inserted into MongoDB.')
        except Exception as e:
            logging.error(f'Error inserting product into MongoDB: {e}')
            raise
    
    def saveToMongo(self):
        try:
            
            product_data = {
                "nome": self.nome,
                "descricao": self.descricao,
                "price": self.price
            }
            db.products.update_one(
                {"_id": ObjectId(self.id)},
                {"$set": product_data}
            )
            logging.debug(f'Product {self.nome} saved to MongoDB.')
        except Exception as e:
            logging.error(f'Error saving product to MongoDB: {e}')
            raise

    def updateInMongo(self):
        try:
            product_data = self.model_dump(by_alias=True, exclude_unset=True)
            product_data.pop('_id', None)
            result = db.products.update_one(
                {"_id": ObjectId(self.id)},
                {"$set": product_data}
            )
            if result.modified_count > 0:
                logging.debug(f'Product {self.nome} updated successfully in MongoDB.')
            else:
                logging.warning(f'Product {self.nome} not found or no changes made in MongoDB.')
        except Exception as e:
            logging.error(f'Error updating product in MongoDB: {e}')
            raise

    @classmethod
    def getByProducts(cls) -> List['Product']:
        try:
            products = db.products.find()
            logging.debug('Products fetched from MongoDB.')
            return [cls(**cls.__adaptDocument(product)) for product in products]
        except Exception as e:
            logging.error(f'Error fetching products from MongoDB: {e}')
            return []

    @classmethod
    def getById(cls, product_id: str) -> Optional['Product']:
        try:
            product = db.products.find_one({"_id": ObjectId(product_id)})
            if product:
                logging.debug(f'Product with id {product_id} fetched from MongoDB.')
                return cls(**cls.__adaptDocument(product))
            else:
                logging.warning(f'Product with id {product_id} not found in MongoDB.')
                return None
        except Exception as e:
            logging.error(f'Error fetching product by id from MongoDB: {e}')
            return None

    @staticmethod
    def __adaptDocument(product_doc: dict) -> dict:
        product_doc['_id'] = str(product_doc['_id'])
        return product_doc

    def addOrUpdateAvaliacao(self, avaliacao: Avaliacao):
        for existing_avaliacao in self.avaliacoes:
            if existing_avaliacao.user_id == avaliacao.user_id:
                existing_avaliacao.estrelas_user = avaliacao.estrelas_user
                existing_avaliacao.comentario_user = avaliacao.comentario_user
                self.updateInMongo()
                return
        self.avaliacoes.append(avaliacao)
        self.updateInMongo()
