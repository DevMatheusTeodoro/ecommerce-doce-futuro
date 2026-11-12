from config.database import conectar

class PedidoModel:
    @staticmethod
    def criar(id_cliente, total, itens):
        conexao = conectar()
        cursor = conexao.cursor()
        
        # 1. Cria o registro do pedido principal
        sql_pedido = "INSERT INTO Pedido (id_cliente, valor_total, status) VALUES (%s, %s, 'Preparando')"
        cursor.execute(sql_pedido, (id_cliente, total))
        id_pedido = cursor.lastrowid
        
        # 2. Insere cada cupcake do carrinho na tabela de itens
        sql_item = "INSERT INTO ItemPedido (id_pedido, id_cupcake, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
        for item in itens:
            cursor.execute(sql_item, (id_pedido, item['id_cupcake'], item['quantidade'], item['preco_unitario']))
            
        conexao.commit()
        cursor.close()
        conexao.close()
        return id_pedido

    @staticmethod
    def buscar_por_cliente(id_cliente):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        # Busca os pedidos do mais recente para o mais antigo
        cursor.execute("SELECT * FROM Pedido WHERE id_cliente = %s ORDER BY id_pedido DESC", (id_cliente,))
        pedidos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return pedidos