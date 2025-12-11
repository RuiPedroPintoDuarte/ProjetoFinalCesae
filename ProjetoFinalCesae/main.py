import pandas as pd
import sqlalchemy
import pyodbc
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/BankDatabase?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Engine SQLAlchemy para operações diretas
engine = sqlalchemy.create_engine(
    "mssql+pyodbc://@localhost/BankDatabase?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# Modelos de Dimensão
class DimCliente(db.Model):
    __tablename__ = 'DimCliente'
    ClienteId = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(120), nullable=True)
    DataNascimento = db.Column(db.Date, nullable=True)
    NIF = db.Column(db.String(20), unique=True, nullable=True)
    Username = db.Column(db.String(120), nullable=False, unique=True)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    PalavraPasse = db.Column(db.String(120), nullable=False)

class DimGestor(db.Model):
    __tablename__ = 'DimGestor'
    GestorId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(120), nullable=False, unique=True)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    PalavraPasse = db.Column(db.String(120), nullable=False)

class DimAdmin(db.Model):
    __tablename__ = 'DimAdmin'
    AdminId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(120), nullable=False, unique=True)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    PalavraPasse = db.Column(db.String(120), nullable=False)

# Novos Modelos de Fato
class FactGestorCliente(db.Model):
    __tablename__ = 'FactGestorCliente'
    GestorId = db.Column(db.Integer, db.ForeignKey('DimGestor.GestorId'), primary_key=True)
    ClienteId = db.Column(db.Integer, db.ForeignKey('DimCliente.ClienteId'), primary_key=True)

class FactTransacao(db.Model):
    __tablename__ = 'FactTransacao'
    TransacaoId = db.Column(db.Integer, primary_key=True)
    ClienteId = db.Column(db.Integer, db.ForeignKey('DimCliente.ClienteId'), nullable=False)
    Descricao = db.Column(db.String(255), nullable=True)
    Quantidade = db.Column(db.Float, nullable=False)
    DataTransacao = db.Column(db.Date, nullable=False)

class FactInfoBancaria(db.Model):
    __tablename__ = 'FactInfoBancaria'
    InfoId = db.Column(db.Integer, primary_key=True)
    ClienteId = db.Column(db.Integer, db.ForeignKey('DimCliente.ClienteId'), nullable=False)
    Emprego = db.Column(db.String(50), nullable=True)
    EstadoCivil = db.Column(db.String(50), nullable=True)
    DefaultCredit = db.Column(db.Boolean, nullable=True)
    Saldo = db.Column(db.Float, nullable=False)
    EmprestimoCasa = db.Column(db.Boolean, nullable=True)
    EmprestimoPessoal = db.Column(db.Boolean, nullable=True)
    DataRegisto = db.Column(db.Date, nullable=False)

# Decorador para verificar autenticação
def autenticacao_obrigatoria(f):
    @wraps(f)
    def funcao_decorada(*args, **kwargs):
        if 'utilizador_id' not in session:
            flash('Por favor, faça login primeiro.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return funcao_decorada

# Decorador para verificar papel
def papel_obrigatorio(papel_requerido):
    def decorador(f):
        @wraps(f)
        def funcao_decorada(*args, **kwargs):
            if 'utilizador_id' not in session:
                flash('Por favor, faça login primeiro.', 'warning')
                return redirect(url_for('login'))

            # Check user type from session
            if session.get('user_type') != papel_requerido:
                flash('Acesso negado. Permissão insuficiente.', 'perigo')
                return redirect(url_for('painel'))
            return f(*args, **kwargs)
        return funcao_decorada
    return decorador

# Rota de Registo
@app.route('/registo', methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        nome = request.form.get('nome')
        data_nascimento_str = request.form.get('data_nascimento')
        nif = request.form.get('nif')
        palavra_passe = request.form.get('palavra_passe')
        
        if DimCliente.query.filter_by(Username=username).first() or DimCliente.query.filter_by(Email=email).first():
            flash('Utilizador já existe!', 'perigo')
            return redirect(url_for('registo'))
        
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date() if data_nascimento_str else None
        
        novo_cliente = DimCliente(Username=username, Email=email, PalavraPasse=palavra_passe, Nome=nome, DataNascimento=data_nascimento, NIF=nif)
        
        db.session.add(novo_cliente)
        db.session.commit()
        
        flash('Conta criada com sucesso! Por favor, faça login.', 'sucesso')
        return redirect(url_for('login'))
    
    return render_template('registo.html')

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        palavra_passe = request.form.get('palavra_passe')
        
        print(f"Tentando login com email: {email}, password: {palavra_passe}")
        
        cliente = DimCliente.query.filter_by(Email=email).first()
        gestor = DimGestor.query.filter_by(Email=email).first()
        admin = DimAdmin.query.filter_by(Email=email).first()
        
        logged_in_user = None
        user_type = None

        if cliente and cliente.PalavraPasse == palavra_passe:
            logged_in_user = cliente
            user_type = 'cliente'
            session['utilizador_id'] = cliente.ClienteId
        elif gestor and gestor.PalavraPasse == palavra_passe:
            logged_in_user = gestor
            user_type = 'gestor'
            session['utilizador_id'] = gestor.GestorId
        elif admin and admin.PalavraPasse == palavra_passe:
            logged_in_user = admin
            user_type = 'admin'
            session['utilizador_id'] = admin.AdminId
        
        if logged_in_user:
            session['username'] = logged_in_user.Username
            session['user_type'] = user_type # Store user type as string
            flash(f'Bem-vindo, {logged_in_user.Username}!', 'sucesso')
            return redirect(url_for('painel'))
        else:
            flash('Email ou palavra-passe incorretos!', 'perigo')
    
    return render_template('login.html')

# Rota Painel (após login)
@app.route('/painel')
@autenticacao_obrigatoria
def painel():
    user_id = session['utilizador_id']
    user_type = session['user_type']
    
    if user_type == 'cliente':
        utilizador = DimCliente.query.get(user_id)
    elif user_type == 'gestor':
        utilizador = DimGestor.query.get(user_id)
    elif user_type == 'admin':
        utilizador = DimAdmin.query.get(user_id)
    
    return render_template('painel.html', utilizador=utilizador, papel=user_type.capitalize())

# Rota para Criar Gestor (apenas Admin)
@app.route('/criar-gestor', methods=['GET', 'POST'])
@papel_obrigatorio('admin')
def criar_gestor():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        palavra_passe = request.form.get('palavra_passe')

        if DimGestor.query.filter_by(Username=username).first() or DimGestor.query.filter_by(Email=email).first():
            flash('Utilizador já existe!', 'perigo')
            return redirect(url_for('criar_gestor'))
        
        novo_gestor = DimGestor(Username=username, Email=email, PalavraPasse=palavra_passe)
        
        db.session.add(novo_gestor)
        db.session.commit()
        
        flash('Gestor criado com sucesso!', 'sucesso')
        return redirect(url_for('painel'))
    
    return render_template('criar_gestor.html')

# Rota para Criar Cliente (Admin e Gestor)
@app.route('/criar-cliente', methods=['GET', 'POST'])
@autenticacao_obrigatoria
def criar_cliente():
    user_type = session['user_type']
    
    if user_type not in ['gestor', 'admin']:
        flash('Acesso negado.', 'perigo')
        return redirect(url_for('painel'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        nome = request.form.get('nome')
        data_nascimento_str = request.form.get('data_nascimento')
        nif = request.form.get('nif')
        palavra_passe = request.form.get('palavra_passe')
        
        if DimCliente.query.filter_by(Username=username).first() or DimCliente.query.filter_by(Email=email).first():
            flash('Utilizador já existe!', 'perigo')
            return redirect(url_for('criar_cliente'))
        
        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date() if data_nascimento_str else None
        novo_cliente = DimCliente(Username=username, Email=email, PalavraPasse=palavra_passe, Nome=nome, DataNascimento=data_nascimento, NIF=nif)
        
        db.session.add(novo_cliente)
        db.session.commit()
        
        flash('Cliente criado com sucesso!', 'sucesso')
        return redirect(url_for('painel'))
    
    return render_template('criar_cliente.html')

# Rota de Logout
@app.route('/terminar-sessao')
def terminar_sessao():
    session.clear()
    flash('Terminou a sessão com sucesso!', 'sucesso')
    return redirect(url_for('login'))

# Rota raiz
@app.route('/')
def index():
    if 'utilizador_id' in session:
        return redirect(url_for('painel'))
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)