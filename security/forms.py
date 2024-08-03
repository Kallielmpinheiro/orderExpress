from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class RegisterForm(FlaskForm):
    nomeCompleto = StringField('Nome Completo', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    dataNascimento = StringField('Data de Nascimento', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class ProductForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    price = DecimalField('Preço', validators=[DataRequired()])
    submit = SubmitField('Criar Produto')
    
    class Meta:
        csrf = False
    
class SuspendUserForm(FlaskForm):
    cpf = StringField('CPF do Usuário', validators=[DataRequired()])
    submit = SubmitField('Banir')

class UnsuspendUserForm(FlaskForm):
    cpf = StringField('CPF do Usuário', validators=[DataRequired()])
    submit = SubmitField('Desbanir')
