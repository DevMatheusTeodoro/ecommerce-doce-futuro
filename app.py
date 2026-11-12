from flask import Flask
from controllers.vitrine_controller import vitrine_bp
from controllers.auth_controller import auth_bp
from controllers.carrinho_controller import carrinho_bp
from controllers.checkout_controller import checkout_bp  # <-- 1. Importe o controller

app = Flask(__name__, template_folder='views')
app.secret_key = 'doce_futuro_mvp_secret'

app.register_blueprint(vitrine_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(carrinho_bp)
app.register_blueprint(checkout_bp)  # <-- 2. Registre o blueprint

if __name__ == '__main__':
    app.run(debug=True)