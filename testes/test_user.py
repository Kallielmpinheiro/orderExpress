import pytest
from classes.user import User
from database.mysql import client, cursor

def testCreateUser():
    user = User(
        nomeCompleto="João da Silvaa",
        cpf="123456789003",
        dataNascimento="1990-01-01",
        email="joao3@example.com",
        senha="senha123",
        telefone="123456789",
        endereco="Rua A, 123"
    )
    User.createUser(user)

def testGetUserByCpf():
    cpf_teste = "123456789002"
    try:
        user = User.getUserByCpf(cpf_teste)

        if user:
            assert user.cpf == cpf_teste
            print(f"Usuário encontrado: {user.nomeCompleto}")
        else:
            pytest.fail(f"Usuário com CPF {cpf_teste} não encontrado")

    except Exception as e:
        pytest.fail(f"Erro ao buscar usuário: {e}")
        
def testGetUserById():
    user_id = 10
    try:
        user = User.getUserById(user_id)

        if user:
            assert user.idUser == user_id
            print(f"Usuário encontrado: {user.nomeCompleto}")
        else:
            pytest.fail(f"Usuário com ID {user_id} não encontrado")

    except Exception as e:
        pytest.fail(f"Erro ao buscar usuário por ID: {e}")
 
def testSuspendUser():
    user = User.getUserByCpf("123456789002")
    assert user.statusConta == "active" or user.statusConta == "banned", f"Status da conta inesperado '{user.statusConta}'"

    user.banir()

    user = User.getUserByCpf("123456789002")
    assert user.statusConta == "banned", f"Status da conta esperado 'banned', mas encontrado '{user.statusConta}'"

def testUnsuspendUser():
    user = User.getUserByCpf("123456789002")
    user.banir()
    assert user.statusConta == "banned", f"Status da conta esperad3o 'banned', mas encontrado '{user.statusConta}'"

    user.desbanir()

    user = User.getUserByCpf("123456789002")
    assert user.statusConta == "active", f"Status da conta esperado 'active', mas encontrado '{user.statusConta}'"