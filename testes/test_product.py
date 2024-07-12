import pytest
from classes.product import Product

def test_criar_produto():
    produto = Product(id_product=1, nome="Produto A", descricao="Descrição do Produto A", price=29.99)
    assert produto.id_product == 1
    assert produto.nome == "Produto A"
    assert produto.descricao == "Descrição do Produto A"
    assert produto.price == 29.99

def test_salvar_no_mongodb():
    produto = Product(id_product=2, nome="Produto B", descricao="Descrição do Produto B", price=39.99)
    Product.save_to_mongo(produto)
