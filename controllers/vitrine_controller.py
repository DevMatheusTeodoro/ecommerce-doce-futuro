from flask import Blueprint, render_template
from models.produto_model import ProdutoModel

vitrine_bp = Blueprint('vitrine', __name__)

@vitrine_bp.route('/')
def index():
    cupcakes = ProdutoModel.listar_disponiveis()
    return render_template('vitrine.html', cupcakes=cupcakes)