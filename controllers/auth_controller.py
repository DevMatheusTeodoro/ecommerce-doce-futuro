from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.cliente_model import ClienteModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if '_flashes' in session:
        session['_flashes'] = [f for f in session['_flashes'] if f[0] != 'success']
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        cliente = ClienteModel.buscar_por_email(email)
        if cliente and check_password_hash(cliente['senha'], senha):
            session['cliente_id'] = cliente['id_cliente']
            session['cliente_nome'] = cliente['nome']
            return redirect(url_for('vitrine.index'))
        
        flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')

    novo_id = ClienteModel.criar(nome, email, senha, telefone)
    if novo_id:
        session['cliente_id'] = novo_id
        session['cliente_nome'] = nome
        return redirect(url_for('vitrine.index'))
    
    flash('Este e-mail já está cadastrado. Tente fazer login.', 'warning')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.pop('cliente_id', None)
    session.pop('cliente_nome', None)
    return redirect(url_for('vitrine.index'))