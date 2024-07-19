from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from classes.user import User
from decorators import admin_required
from classes.product import Product

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    if current_user.is_authenticated:
        user_type = current_user.tipoUser
    else:
        user_type = None
        
    products = Product.getByProducts()
    for product in products:
        print(f"Produto: {product.nome}, Preço: {product.price}")
    return render_template('index.html', user_type=user_type, products=products)

@user_bp.route('/admin')
@admin_required
def indexadmin():
    if current_user.is_authenticated:
        user_type = current_user.tipoUser
    else:
        user_type = None
    return render_template('admin.html', user_type=user_type)
        

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        password = request.form['password']

        user = User.getUserByCpf(cpf)
        if user:
            if user.senha == password:
                if user.statusConta == 'active':
                    login_user(user)
                    return redirect(url_for('user.index'))
                else:
                    flash('Sua conta está suspensa. Entre em contato com o administrador.')
            else:
                flash('Senha incorreta.')
        else:
            flash('CPF não encontrado.')

    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user_bp.route('/redirect')
@login_required
def redirect_page():
    return render_template('redirect.html')

@user_bp.route('/suspend_user', methods=['POST'])
@login_required
@admin_required
def suspend_user():
    if current_user.tipoUser == 'admin':
        cpf = request.form['cpf']
        user = User.getUserByCpf(cpf)
        
        if user:
            user.banir()
            flash(f'Usuário com CPF {cpf} suspenso com sucesso')
            print(f'Usuário com CPF {cpf} suspenso com sucesso')
        else:
            flash('Usuário não encontrado')
            print('Usuário não encontrado')
            return redirect(url_for('user.indexadmin'))

    else:
        flash('Apenas administradores podem suspender usuários')
        print('Apenas administradores podem suspender usuários')
        return redirect(url_for('user.index'))
    return redirect(url_for('user.indexadmin'))
    
@user_bp.route('/unsuspend_user', methods=['POST'])
@login_required
@admin_required
def unsuspend_user():
    if current_user.tipoUser == 'admin':
        cpf = request.form['cpf']
        user = User.getUserByCpf(cpf)
        if user:
            user.desbanir()
            flash(f'Usuário com CPF {cpf} desbanido com sucesso')
            print(f'Usuário com CPF {cpf} desbanido com sucesso')
        else:
            flash('Usuário não encontrado')
            print('Usuário não encontrado')
        return redirect(url_for('user.indexadmin'))
    else:
        flash('Apenas administradores podem desbanir usuários')
        print('Apenas administradores podem desbanir usuários')
        return redirect(url_for('user.indexadmin'))
    
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            user_data = {
                "nomeCompleto": request.form['nomeCompleto'],
                "cpf": request.form['cpf'],
                "dataNascimento": request.form['dataNascimento'],
                "email": request.form['email'],
                "senha": request.form['senha'],
                "telefone": request.form['telefone'],
                "endereco": request.form['endereco'],
                "tipoUser": 'customer',
                "statusConta": 'active'
            }
            user = User(**user_data)
            User.createUser(user)
            flash(f'Usuário {user.nomeCompleto} criado com sucesso!')
            return redirect(url_for('user.login'))
        except Exception as e:
            flash(f'Ocorreu um erro ao criar o usuário: {e}')
            return redirect(url_for('user.register'))
    return render_template('register.html')
    