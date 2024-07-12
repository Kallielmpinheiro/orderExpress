import pytest
from classes.pedidoOrder import Pedido

def test_criar_pedido():
    pedido = Pedido(id_pedido=1, id_cliente=123, produtos=["Produto A"], total=100.0)
    assert pedido.id_pedido == 1
    assert pedido.id_cliente == 123
    assert pedido.produtos == ["Produto A"]
    assert pedido.total == 100.0
    assert pedido.status == "Pendente"
