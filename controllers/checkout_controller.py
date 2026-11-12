from flask import Blueprint, render_template, redirect, url_for, session, flash
from models.pedido_model import PedidoModel

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout')
def finalizar_compra():
    # Verifica se o usuário está logado
    if 'cliente_id' not in session:
        flash('Faça login ou cadastre-se para finalizar sua compra.', 'warning')
        return redirect(url_for('auth.login'))
        
    carrinho = session.get('carrinho', {})
    if not carrinho:
        return redirect(url_for('vitrine.index'))
        
    # Calcula o total
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())
    
    # Prepara a lista de itens iterando pelo dicionário da sessão
    itens = []
    for id_cupcake, dados in carrinho.items():
        itens.append({
            'id_cupcake': id_cupcake,
            'quantidade': dados['quantidade'],
            'preco_unitario': dados['preco']
        })
        
    # Registra no MySQL
    PedidoModel.criar(session['cliente_id'], total, itens)
    
    # Esvazia o carrinho após a compra
    session.pop('carrinho', None)
    flash('Pedido realizado com sucesso!', 'success')
    
    return redirect(url_for('checkout.rastreio'))

@checkout_bp.route('/rastreio')
def rastreio():
    if 'cliente_id' not in session:
        return redirect(url_for('auth.login'))
        
    pedidos = PedidoModel.buscar_por_cliente(session['cliente_id'])
    return render_template('rastreio.html', pedidos=pedidos)