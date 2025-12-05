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

# Modelo de Utilizador
class Utilizador(db.Model):
    __tablename__ = 'Utilizador'
    UtilizadorId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(120), nullable=False, unique=True)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    PalavraPasse = db.Column(db.String(120), nullable=False)
    TipoUtilizador = db.Column(db.Integer, nullable=False)  # 1-cliente, 2-gestor, 3-admin

# Decorador para verificar autenticação
def autenticacao_obrigatoria(f):
    @wraps(f)
    def funcao_decorada(*args, **kwargs):
        if 'utilizador_id' not in session:
            flash('Por favor, faça login primeiro.', 'aviso')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return funcao_decorada

# Decorador para verificar papel
def papel_obrigatorio(papel_requerido):
    def decorador(f):
        @wraps(f)
        def funcao_decorada(*args, **kwargs):
            if 'utilizador_id' not in session:
                flash('Por favor, faça login primeiro.', 'aviso')
                return redirect(url_for('login'))

            utilizador = Utilizador.query.get(session['utilizador_id'])
            if utilizador.TipoUtilizador != papel_requerido:
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
        palavra_passe = request.form.get('palavra_passe')
        
        if Utilizador.query.filter_by(Username=username).first():
            flash('Utilizador já existe!', 'perigo')
            return redirect(url_for('registo'))
        
        novo_utilizador = Utilizador(Username=username, Email=email, PalavraPasse=palavra_passe, TipoUtilizador=1)
        
        db.session.add(novo_utilizador)
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
        
        utilizador = Utilizador.query.filter_by(Email=email).first()
        print(f"Utilizador encontrado: {utilizador}")
        
        if utilizador:
            print(f"Password BD: {utilizador.PalavraPasse}")
            print(f"Password recebida: {palavra_passe}")
            print(f"Passwords iguais: {utilizador.PalavraPasse == palavra_passe}")
        
        if utilizador and utilizador.PalavraPasse == palavra_passe:
            session['utilizador_id'] = utilizador.UtilizadorId
            session['username'] = utilizador.Username
            session['papel'] = utilizador.TipoUtilizador
            flash(f'Bem-vindo, {utilizador.Username}!', 'sucesso')
            return redirect(url_for('painel'))
        else:
            flash('Email ou palavra-passe incorretos!', 'perigo')
    
    return render_template('login.html')

# Rota Painel (após login)
@app.route('/painel')
@autenticacao_obrigatoria
def painel():
    utilizador = Utilizador.query.get(session['utilizador_id'])
    nomes_papel = {1: 'Cliente', 2: 'Gestor', 3: 'Administrador'}
    return render_template('painel.html', utilizador=utilizador, papel=nomes_papel[utilizador.TipoUtilizador])

# Rota para Criar Gestor (apenas Admin)
@app.route('/criar-gestor', methods=['GET', 'POST'])
@papel_obrigatorio(3)
def criar_gestor():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        palavra_passe = request.form.get('palavra_passe')
        
        if Utilizador.query.filter_by(Username=username).first():
            flash('Utilizador já existe!', 'perigo')
            return redirect(url_for('criar_gestor'))
        
        novo_gestor = Utilizador(Username=username, Email=email, PalavraPasse=palavra_passe, TipoUtilizador=2)
        
        db.session.add(novo_gestor)
        db.session.commit()
        
        flash('Gestor criado com sucesso!', 'sucesso')
        return redirect(url_for('painel'))
    
    return render_template('criar_gestor.html')

# Rota para Criar Cliente (Admin e Gestor)
@app.route('/criar-cliente', methods=['GET', 'POST'])
@autenticacao_obrigatoria
def criar_cliente():
    utilizador = Utilizador.query.get(session['utilizador_id'])
    
    if utilizador.TipoUtilizador not in [2, 3]:
        flash('Acesso negado.', 'perigo')
        return redirect(url_for('painel'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        palavra_passe = request.form.get('palavra_passe')
        
        if Utilizador.query.filter_by(Username=username).first():
            flash('Utilizador já existe!', 'perigo')
            return redirect(url_for('criar_cliente'))
        
        novo_cliente = Utilizador(Username=username, Email=email, PalavraPasse=palavra_passe, TipoUtilizador=1)
        
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