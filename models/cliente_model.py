import mysql.connector
from werkzeug.security import generate_password_hash
from config.database import conectar

class ClienteModel:
    @staticmethod
    def criar(nome, email, senha, telefone):
        conexao = conectar()
        cursor = conexao.cursor()
        senha_hash = generate_password_hash(senha)
        try:
            sql = "INSERT INTO Cliente (nome, email, senha, telefone) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, email, senha_hash, telefone))
            conexao.commit()
            return cursor.lastrowid
        except mysql.connector.IntegrityError:
            return None 
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def buscar_por_email(email):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Cliente WHERE email = %s", (email,))
        cliente = cursor.fetchone()
        cursor.close()
        conexao.close()
        return cliente