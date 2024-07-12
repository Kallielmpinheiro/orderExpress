import pytest
from classes.product import Product

def testCriarProduto():
    produto = Product(id_product=1, nome="Produto A", descricao="Descrição do Produto A", price=29.99)
    assert produto.id_product == 1
    assert produto.nome == "Produto A"
    assert produto.descricao == "Descrição do Produto A"
    assert produto.price == 29.99

def testSalvarMongodb():
    produto = Product(id_product=2, nome="Produto B", descricao="Descrição do Produto B", price=39.99)
    Product.saveToMongo(produto)
