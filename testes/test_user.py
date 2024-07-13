import pytest
from classes.user import User

# def testCreateUser():
#     user = User(
#         nomeCompleto="João da Silvaa",
#         cpf="123456789001",
#         dataNascimento="1990-01-01",
#         email="joao@example.com",
#         senha="senha123",
#         telefone="123456789",
#         endereco="Rua A, 123"
#     )
#     User.createUser(user)

def test_get_user_by_cpf():
    cpf_teste = "123456789001"
    try:
        user = User.getUserByCpf(cpf_teste)

        if user:
            assert user.cpf == cpf_teste
            print(f"Usuário encontrado: {user.nomeCompleto}")
        else:
            pytest.fail(f"Usuário com CPF {cpf_teste} não encontrado")

    except Exception as e:
        pytest.fail(f"Erro ao buscar usuário: {e}")
        
def test_get_user_by_id():
    user_id = 4
    try:
        user = User.getUserById(user_id)

        if user:
            assert user.idUser == user_id
            print(f"Usuário encontrado: {user.nomeCompleto}")
        else:
            pytest.fail(f"Usuário com ID {user_id} não encontrado")

    except Exception as e:
        pytest.fail(f"Erro ao buscar usuário por ID: {e}")