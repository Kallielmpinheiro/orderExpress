from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from classes.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        password = request.form['password']

        user = User.getUserByCpf(cpf)
        if user and user.senha == password:
            login_user(user)
            return redirect(url_for('auth.redirect_page'))

        flash('CPF ou senha incorretos')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/redirect')
@login_required
def redirect_page():
    return render_template('redirect.html')
