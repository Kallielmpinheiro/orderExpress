from pydantic import BaseModel, Field
from database.mysql import client
from flask_login import UserMixin

class User(BaseModel, UserMixin):
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

    # Métodos exigidos pelo Flask-Login
    
    @property
    def isActive(self):
        return self.statusConta == "active"

    @property
    def isAuthenticated(self):
        return True

    @property
    def isAnonymous(self):
        return False

    def get_id(self):
        return str(self.idUser)
    
    def banir(self):
        query = "UPDATE User SET statusConta = 'banned' WHERE cpf = %s"
        cursor = client.cursor()
        try:
            cursor.execute(query, (self.cpf,))
            client.commit()
            self.statusConta = 'banned'
            print(f"Usuário com CPF {self.cpf} banido com sucesso!")
        except Exception as e:
            print(f"Erro ao banir usuário: {e}")
        finally:
            cursor.close()

    def desbanir(self):
        query = "UPDATE User SET statusConta = 'active' WHERE cpf = %s"
        cursor = client.cursor()
        try:
            cursor.execute(query, (self.cpf,))
            client.commit()
            self.statusConta = 'active'
            print(f"Usuário com CPF {self.cpf} desbanido com sucesso!")
        except Exception as e:
            print(f"Erro ao desbanir usuário: {e}")
        finally:
            cursor.close()
            
    def getByUserGetStatus(cls, statusConta: str) -> "User":
        query = "SELECT * FROM User WHERE statusConta = %s"
        cursor = client.cursor(dictionary=True)
        cursor.execute(query, (statusConta,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            result["dataNascimento"] = str(result["dataNascimento"])
            return User(**result)
        return None

