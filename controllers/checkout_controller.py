from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.pedido_model import PedidoModel

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout', methods=['GET'])
def index():
    if 'cliente_id' not in session:
        flash('Faça login ou cadastre-se para prosseguir com o checkout.', 'warning')
        return redirect(url_for('auth.login'))
        
    carrinho = session.get('carrinho', {})
    if not carrinho:
        return redirect(url_for('vitrine.index'))
        
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())
    return render_template('checkout.html', carrinho=carrinho, total=total)

@checkout_bp.route('/checkout/finalizar', methods=['POST'])
def finalizar():
    if 'cliente_id' not in session:
        return redirect(url_for('auth.login'))
        
    carrinho = session.get('carrinho', {})
    if not carrinho:
        return redirect(url_for('vitrine.index'))
        
    cep = request.form.get('cep')
    logradouro = request.form.get('logradouro')
    numero = request.form.get('numero')
    complemento = request.form.get('complemento', '') 
    pagamento = request.form.get('pagamento')
    
    if not cep or not logradouro or not numero or not pagamento:
        flash('Preencha todos os dados obrigatórios de entrega e pagamento.', 'danger')
        return redirect(url_for('checkout.index'))
        
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())
    
    itens = []
    for id_cupcake, dados in carrinho.items():
        itens.append({
            'id_cupcake': id_cupcake,
            'quantidade': dados['quantidade'],
            'preco_unitario': dados['preco']
        })
        
    PedidoModel.criar(session['cliente_id'], total, itens, cep, logradouro, numero, complemento, pagamento)
    
    session.pop('carrinho', None)
    flash('Pedido realizado com sucesso!', 'success')
    
    return redirect(url_for('checkout.rastreio'))

@checkout_bp.route('/rastreio')
def rastreio():
    if 'cliente_id' not in session:
        return redirect(url_for('auth.login'))
        
    pedidos = PedidoModel.buscar_por_cliente(session['cliente_id'])
    return render_template('rastreio.html', pedidos=pedidos)