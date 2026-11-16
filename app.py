from flask import Flask, session
from controllers.vitrine_controller import vitrine_bp
from controllers.auth_controller import auth_bp
from controllers.carrinho_controller import carrinho_bp
from controllers.checkout_controller import checkout_bp

app = Flask(__name__, template_folder='views')
app.secret_key = 'doce_futuro_mvp_secret'

@app.context_processor
def injetar_total_carrinho():
    carrinho = session.get('carrinho', {})
    total_unidades = sum(int(item.get('quantidade', 0)) for item in carrinho.values())
    return {'total_carrinho': total_unidades}

app.register_blueprint(vitrine_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(carrinho_bp)
app.register_blueprint(checkout_bp)

if __name__ == '__main__':
    app.run(debug=True)