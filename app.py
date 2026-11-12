from flask import Flask
from controllers.vitrine_controller import vitrine_bp

app = Flask(__name__, template_folder='views')
app.secret_key = 'doce_futuro_mvp_secret'

app.register_blueprint(vitrine_bp)

if __name__ == '__main__':
    app.run(debug=True)