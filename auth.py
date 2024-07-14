from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from classes.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        user_type = current_user.tipoUser
    else:
        user_type = None
    return render_template('index.html', user_type=user_type)

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

@auth_bp.route('/suspend_user', methods=['POST'])
@login_required
def suspendUser():
    if current_user.tipoUser == 'admin':
        cpf = request.form['cpf']
        user = User.getUserByCpf(cpf)
        if user:
            user.suspender()
            flash(f'Usuário com CPF {cpf} suspenso com sucesso')
        else:
            flash('Usuário não encontrado')
        return redirect(url_for('auth.index'))
    else:
        flash('Apenas administradores podem suspender usuários')
        return redirect(url_for('auth.index'))
    
@auth_bp.route('/unsuspend_user', methods=['POST'])
@login_required
def unsuspendUser():
    if current_user.tipoUser == 'admin':
        cpf = request.form['cpf']
        user = User.getUserByCpf(cpf)
        if user:
            user.desbanir()
            flash(f'Usuário com CPF {cpf} desbanido com sucesso')
        else:
            flash('Usuário não encontrado')
        return redirect(url_for('auth.index'))
    else:
        flash('Apenas administradores podem desbanir usuários')
        return redirect(url_for('auth.index'))