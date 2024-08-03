from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from classes.user import User
from decorators import admin_required
from classes.product import Product
from database.mongodb import db
from bson import ObjectId
from security.forms import LoginForm, RegisterForm, SuspendUserForm, UnsuspendUserForm, ProductForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    if current_user.is_authenticated:
        user_type = current_user.tipoUser
        
    else:
        user_type = None

    products = Product.getByProducts()
    for product in products:
        product.avaliacoes = list(db.reviews.find({'product_id': ObjectId(product.id)}))
        for avaliacao in product.avaliacoes:
            avaliacao['username'] = User.get_user_name_by_cpf(avaliacao['user_cpf'])

        if current_user.is_authenticated:
            product.already_reviewed = any(avaliacao['user_cpf'] == current_user.cpf for avaliacao in product.avaliacoes)
        else:
            product.already_reviewed = False

    return render_template('index.html', user_type=user_type, products=products)

@user_bp.route('/admin')
@admin_required
def indexadmin():
    if current_user.is_authenticated:
        user_type = current_user.tipoUser
        form_suspend = SuspendUserForm()
        form_unsuspend = UnsuspendUserForm()
        form_product = ProductForm()
    else:
        user_type = None
    return render_template('admin.html', user_type=user_type, form_suspend=form_suspend, form_unsuspend=form_unsuspend,form_product=form_product)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cpf = form.cpf.data
        password = form.password.data

        user = User.getUserByCpf(cpf)
        if user and user.senha == password:
            if user.statusConta == 'active':
                login_user(user)
                return redirect(url_for('user.index'))
            else:
                flash('Sua conta está suspensa. Entre em contato com o administrador.')
        else:
            flash('CPF ou senha incorretos.')

    return render_template('login.html', form=form)

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
    form = SuspendUserForm(request.form)
    if form.validate_on_submit():
        cpf = form.cpf.data
        if current_user.tipoUser == 'admin':
            user = User.getUserByCpf(cpf)
            if user:
                user.banir()
                flash(f'Usuário com CPF {cpf} banido com sucesso')
                print(f'Usuário com CPF {cpf} banido com sucesso')
            else:
                flash('Usuário não encontrado')
                print('Usuário não encontrado')
        else:
            flash('Apenas administradores podem banir usuários')
            print('Apenas administradores podem banir usuários')
        return redirect(url_for('user.indexadmin'))
    
    
    return redirect(url_for('user.indexadmin'))

@user_bp.route('/unsuspend_user', methods=['POST'])
@login_required
@admin_required
def unsuspend_user():
    form = UnsuspendUserForm(request.form)
    if form.validate_on_submit():
        cpf = form.cpf.data
        if current_user.tipoUser == 'admin':
            user = User.getUserByCpf(cpf)
            if user:
                user.desbanir()
                flash(f'Usuário com CPF {cpf} desbanido com sucesso')
                print(f'Usuário com CPF {cpf} desbanido com sucesso')
            else:
                flash('Usuário não encontrado')
                print('Usuário não encontrado')
        else:
            flash('Apenas administradores podem desbanir usuários')
            print('Apenas administradores podem desbanir usuários')
        return redirect(url_for('user.indexadmin'))
    
    return redirect(url_for('user.indexadmin'))
        
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user_data = {
                "nomeCompleto": form.nomeCompleto.data,
                "cpf": form.cpf.data,
                "dataNascimento": form.dataNascimento.data,
                "email": form.email.data,
                "senha": form.senha.data,
                "telefone": form.telefone.data,
                "endereco": form.endereco.data,
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
    return render_template('register.html', form=form)
