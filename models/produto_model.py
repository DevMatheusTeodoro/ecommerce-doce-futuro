from config.database import conectar

class ProdutoModel:
    @staticmethod
    def listar_disponiveis():
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Produto WHERE estoque > 0")
        produtos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return produtos