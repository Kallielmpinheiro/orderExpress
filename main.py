from flask import Flask, abort, render_template
from flask_login import LoginManager, current_user
from auth.auth_users import user_bp
from auth.auth_product import product_bp
from auth.auth_pedidos import pedidos_bp
from auth.auth_cart import cart_bp
from auth.auth_vAlalysis import vendas_bp
from auth.auth_avaliacao import avaliacao_bp
from classes.user import User
import os
from dotenv import load_dotenv
import logging


load_dotenv()
app = Flask(__name__, template_folder='view',static_folder='static')
app.secret_key = os.getenv('secret_key')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(vendas_bp)
app.register_blueprint(avaliacao_bp)

logging.getLogger('pymongo').setLevel(logging.ERROR)


if __name__ == '__main__':
    app.run(debug=True)
