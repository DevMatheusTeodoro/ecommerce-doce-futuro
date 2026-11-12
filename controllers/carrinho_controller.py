from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.produto_model import ProdutoModel

carrinho_bp = Blueprint('carrinho', __name__)

@carrinho_bp.route('/carrinho')
def index():
    # Puxa o carrinho da sessão ou cria um dicionário vazio
    carrinho = session.get('carrinho', {})
    total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())
    return render_template('carrinho.html', carrinho=carrinho, total=total)

@carrinho_bp.route('/carrinho/adicionar', methods=['POST'])
def adicionar():
    id_cupcake = request.form.get('id_cupcake')
    quantidade = int(request.form.get('quantidade', 1))

    produto = ProdutoModel.buscar_por_id(id_cupcake)
    
    if produto:
        if 'carrinho' not in session:
            session['carrinho'] = {}
        
        carrinho = session['carrinho']
        
        # Se o cupcake já está no carrinho, apenas soma a quantidade
        if id_cupcake in carrinho:
            carrinho[id_cupcake]['quantidade'] += quantidade
        else:
            carrinho[id_cupcake] = {
                'nome': produto['nome'],
                'preco': float(produto['preco']),
                'quantidade': quantidade
            }
        
        session.modified = True
        flash(f"{produto['nome']} adicionado ao carrinho!", 'success')
        
    return redirect(url_for('vitrine.index'))

@carrinho_bp.route('/carrinho/remover/<id_cupcake>')
def remover(id_cupcake):
    if 'carrinho' in session and id_cupcake in session['carrinho']:
        del session['carrinho'][id_cupcake]
        session.modified = True
    return redirect(url_for('carrinho.index'))