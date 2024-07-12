import pytest
from classes.user import User

def testCreateUser():
    user = User(
        nomeCompleto="João da Silvaa",
        cpf="123456789001",
        dataNascimento="1990-01-01",
        email="joao@example.com",
        senha="senha123",
        telefone="123456789",
        endereco="Rua A, 123"
    )
    User.createUser(user)
