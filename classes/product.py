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

    def saveToMongo(self):
        product_data = self.dict(by_alias=True, exclude_unset=True)
        result = db.products.insert_one(product_data)
        print(f"Produto {self.nome} salvo no MongoDB com o ID: {result.inserted_id}")
        return result.inserted_id

    def updateInMongo(self):
        product_data = self.dict(by_alias=True, exclude_unset=True)
        result = db.products.update_one({"_id": self.id}, {"$set": product_data})
        if result.modified_count > 0:
            print(f"Produto {self.nome} atualizado com sucesso!")
        else:
            print(f"Produto {self.nome} não encontrado ou nenhuma alteração foi feita.")

    @classmethod
    def getByProducts(cls) -> List['Product']:
        products = db.products.find()
        return [cls(**cls.__adaptDocument(product)) for product in products]

    @classmethod
    def getById(cls, product_id: str) -> Optional['Product']:
        product = db.products.find_one({"_id": ObjectId(product_id)})
        if product:
            return cls(**cls.__adaptDocument(product))
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
