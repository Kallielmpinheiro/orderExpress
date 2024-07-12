import pytest
from classes.pedidoOrder import Pedido

def testCriarPedido():
    pedido = Pedido(id_pedido=1, id_cliente=123, produtos=["Produto A", "Produto B"], total=59.98)
    assert pedido.id_pedido == 1
    assert pedido.id_cliente == 123
    assert pedido.produtos == ["Produto A", "Produto B"]
    assert pedido.total == 59.98
    assert pedido.status == "Pendente"

def testSalvarMongodb():
    pedido = Pedido(id_pedido=2, id_cliente=456, produtos=["Produto C", "Produto D"], total=79.98)
    Pedido.enteringMongo(pedido)
