from pydantic import BaseModel, Field
from database.mysql import client

class User(BaseModel):
    idUser: int = Field(None, alias="idUser")
    nomeCompleto: str
    cpf: str
    dataNascimento: str
    email: str
    senha: str
    telefone: str
    endereco: str
    tipoUser: str = "customer"
    statusConta: str = "active"

    @staticmethod
    def createUser(user: "User"):
        query = """
            INSERT INTO User 
            (nomeCompleto, cpf, dataNascimento, email, senha, telefone, endereco, tipoUser, statusConta) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = client.cursor()
        user_data = user.dict(exclude={"idUser"})
        cursor.execute(query, (
            user_data["nomeCompleto"], user_data["cpf"], user_data["dataNascimento"],
            user_data["email"], user_data["senha"], user_data["telefone"],
            user_data["endereco"], user_data["tipoUser"], user_data["statusConta"]
        ))
        client.commit()
        cursor.close()
        print(f"Usuário {user.nomeCompleto} criado com sucesso!")

    @staticmethod
    def getUserById(user_id: int) -> "User":
        query = "SELECT * FROM User WHERE idUser = %s"
        cursor = client.cursor(dictionary=True)
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            result['dataNascimento'] = str(result['dataNascimento'])
            return User(**result)
        return None

    @classmethod
    def getUserByCpf(cls, cpf: str) -> "User":
        query = "SELECT * FROM User WHERE cpf = %s"
        cursor = client.cursor(dictionary=True)
        cursor.execute(query, (cpf,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            result["dataNascimento"] = str(result["dataNascimento"])
            return User(**result)
        return None
