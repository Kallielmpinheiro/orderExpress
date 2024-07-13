from flask import Flask
from flask_login import LoginManager
from auth import auth_bp
from classes.user import User

app = Flask(__name__, template_folder='view',static_folder='static')
app.secret_key = 'L1234'

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
