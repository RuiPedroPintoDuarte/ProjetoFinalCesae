from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from functools import wraps
from sqlalchemy import func, text
import joblib
import pandas as pd
import numpy as np
import statsmodels.api as sm
from Repository import ClientRepository

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/BankDatabase?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
# Em produção, esta chave deve ser carregada de uma variável de ambiente e não estar hardcoded.
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Modelos de Dimensão
class DimCliente(db.Model):
    __tablename__ = 'DimCliente'
    ClienteId = db.Column(db.Integer, primary_key=True, autoincrement=False)
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

class FactEmprestimo(db.Model):
    __tablename__ = 'FactEmprestimo'
    EmprestimoId = db.Column(db.Integer, primary_key=True)
    ClienteId = db.Column(db.Integer, db.ForeignKey('DimCliente.ClienteId'), nullable=False)
    Valor = db.Column(db.Float, nullable=False)
    TipoEmprestimo = db.Column(db.String(50), nullable=False)
    DataPedido = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    ProbabilidadeDefault = db.Column(db.Float, nullable=True)

class FactTransacao(db.Model):
    __tablename__ = 'FactTransacao'
    TransacaoId = db.Column(db.Integer, primary_key=True)
    ClienteId = db.Column(db.Integer, db.ForeignKey('DimCliente.ClienteId'), nullable=False)
    Descricao = db.Column(db.String(255), nullable=True)
    Categoria = db.Column(db.String(50), nullable=True)
    Quantidade = db.Column(db.Float, nullable=False)
    DataTransacao = db.Column(db.Date, nullable=False)

class FactInfoBancaria(db.Model):
    __tablename__ = 'FactInfoBancaria'
    ClienteId = db.Column(db.Integer, db.ForeignKey('DimCliente.ClienteId'), primary_key=True)
    Emprego = db.Column(db.String(50), nullable=True)
    EstadoCivil = db.Column(db.String(50), nullable=True)
    Educacao = db.Column(db.String(50), nullable=True)
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
def papel_obrigatorio(papeis_requeridos):
    if not isinstance(papeis_requeridos, list):
        papeis_requeridos = [papeis_requeridos]
    def decorador(f):
        @wraps(f)
        def funcao_decorada(*args, **kwargs):
            if 'utilizador_id' not in session:
                flash('Por favor, faça login primeiro.', 'warning')
                return redirect(url_for('login'))

            # Check user type from session
            if session.get('user_type') not in papeis_requeridos:
                flash('Acesso negado. Permissão insuficiente.', 'perigo')
                return redirect(url_for('painel'))
            return f(*args, **kwargs)
        return funcao_decorada
    return decorador

# Função auxiliar para formatar números (PT)
def formatar_numero_pt(valor):
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

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
        
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date() if data_nascimento_str else None
        except ValueError:
            flash('Formato de data inválido. Use AAAA-MM-DD.', 'perigo')
            return redirect(url_for('registo'))

        # TODO: A palavra-passe está a ser guardada em texto simples. Implementar hashing.
        novo_id = ClientRepository.getNextId()
        if ClientRepository.verificarClienteId(novo_id):
            flash('Erro: ID de cliente já existe. Tente novamente.', 'perigo')
            return redirect(url_for('criar_cliente'))

        novo_cliente = DimCliente(ClienteId=novo_id, Username=username, Email=email, PalavraPasse=palavra_passe, Nome=nome, DataNascimento=data_nascimento, NIF=nif)
        
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
        
        cliente = DimCliente.query.filter_by(Email=email).first()
        gestor = DimGestor.query.filter_by(Email=email).first()
        admin = DimAdmin.query.filter_by(Email=email).first()
        
        logged_in_user = None
        user_type = None

        # TODO: A verificação da palavra-passe é feita em texto simples. Implementar verificação com hash.
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
            session['user_type'] = user_type
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
        utilizador = db.session.get(DimCliente, user_id)
    elif user_type == 'gestor':
        utilizador = db.session.get(DimGestor, user_id)
    elif user_type == 'admin':
        utilizador = db.session.get(DimAdmin, user_id)
    
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
        
        # TODO: A palavra-passe está a ser guardada em texto simples. Implementar hashing.
        novo_gestor = DimGestor(Username=username, Email=email, PalavraPasse=palavra_passe)
        
        db.session.add(novo_gestor)
        db.session.commit()
        
        flash('Gestor criado com sucesso!', 'sucesso')
        return redirect(url_for('painel'))
    
    return render_template('criar_gestor.html')

# Rota para Criar Cliente (Admin e Gestor)
@app.route('/criar-cliente', methods=['GET', 'POST'])
@papel_obrigatorio(['gestor', 'admin'])
def criar_cliente():
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
        
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date() if data_nascimento_str else None
        except ValueError:
            flash('Formato de data inválido. Use AAAA-MM-DD.', 'perigo')
            return redirect(url_for('criar_cliente'))

        # TODO: A palavra-passe está a ser guardada em texto simples. Implementar hashing.
        novo_id = ClientRepository.getNextId()
        if ClientRepository.verificarClienteId(novo_id):
            flash('Erro: ID de cliente já existe.', 'perigo')
            return redirect(url_for('criar_cliente'))

        novo_cliente = DimCliente(ClienteId=novo_id, Username=username, Email=email, PalavraPasse=palavra_passe, Nome=nome, DataNascimento=data_nascimento, NIF=nif)
        
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

# --- ROTAS CLIENTE ---

@app.route('/meus-movimentos')
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def meus_movimentos():
    user_id = session['utilizador_id']
    cliente = db.session.get(DimCliente, user_id)
    
    # Obter saldo e info bancária
    info_bancaria = FactInfoBancaria.query.filter_by(ClienteId=user_id).first()
    saldo = info_bancaria.Saldo if info_bancaria else 0.0

    # Usar SQL puro para contornar o problema do modelo FactTransacao não ter uma PK correspondente na BD
    sql_query = text("""
        SELECT TOP 10 Descricao, Quantidade, DataTransacao
        FROM FactTransacao
        WHERE ClienteId = :user_id
        ORDER BY DataTransacao DESC
    """)
    transacoes = db.session.execute(sql_query, {'user_id': user_id}).fetchall()
    
    return render_template('cliente_movimentos.html', cliente=cliente, saldo=saldo, transacoes=transacoes)

@app.route('/minha-atividade')
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def minha_atividade():
    user_id = session['utilizador_id']
    
    # Agregação para o gráfico de barras (Total Gasto/Mês)
    # Exemplo: Soma quantidades negativas (gastos) agrupadas por mês
    # NOTA: Agrupar também por ano para não misturar dados de anos diferentes.
    # Usar SQL puro para contornar o problema do modelo FactTransacao
    sql_query = text("""
        SELECT
            YEAR(DataTransacao) as ano,
            MONTH(DataTransacao) as mes,
            SUM(QtdAjustada) as total
        FROM (
            SELECT 
                DataTransacao,
                CASE 
                    WHEN Quantidade < 0 THEN Quantidade
                    WHEN Descricao LIKE N'Empréstimo%' OR Descricao LIKE 'Emprestimo%' THEN -Quantidade
                    ELSE 0 
                END as QtdAjustada
            FROM FactTransacao
            WHERE ClienteId = :user_id
        ) AS Valores
        WHERE QtdAjustada < 0
        GROUP BY YEAR(DataTransacao), MONTH(DataTransacao)
        ORDER BY ano, mes
    """)
    gastos_por_mes = db.session.execute(sql_query, {'user_id': user_id}).fetchall()


    # Passar estes dados para o Chart.js no frontend
    labels = [f"{d.ano}-{d.mes:02d}" for d in gastos_por_mes]
    values = [abs(d.total) for d in gastos_por_mes] # Valor absoluto para o gráfico

    return render_template('cliente_atividade.html', labels=labels, values=values)


@app.route('/meu-perfil')
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def meu_perfil():
    user_id = session['utilizador_id']
    cliente = db.session.get(DimCliente, user_id)
    info = FactInfoBancaria.query.filter_by(ClienteId=user_id).first()
    
    return render_template('cliente_perfil.html', cliente=cliente, info=info)

# --- ROTAS GESTOR / ADMIN (GESTÃO DE CLIENTES) ---

@app.route('/lista-clientes', methods=['GET'])
@papel_obrigatorio(['gestor', 'admin'])
def lista_clientes():
    search_query = request.args.get('q')
    user_type = session.get('user_type')
    user_id = session.get('utilizador_id')
    
    query = DimCliente.query

    if user_type == 'gestor':
        query = query.join(FactGestorCliente, DimCliente.ClienteId == FactGestorCliente.ClienteId)\
                     .filter(FactGestorCliente.GestorId == user_id)
    
    if search_query:
        # Pesquisa por nome ou NIF
        query = query.filter(
            (DimCliente.Nome.contains(search_query)) | 
            (DimCliente.NIF.contains(search_query))
        )

    clientes = query.all()

    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/detalhe-cliente/<int:id>')
@papel_obrigatorio(['gestor', 'admin'])
def detalhe_cliente(id):
    cliente = db.get_or_404(DimCliente, id)
    info = FactInfoBancaria.query.filter_by(ClienteId=id).first()

    # Lógica Simulada de Credit Score para o Gráfico
    score = 0
    if info:
        if not info.DefaultCredit: score += 50
        if info.Saldo > 1000: score += 20
        if info.Emprego: score += 30
    
    # Dados para o gráfico circular (Pie Chart)
    chart_data = {'Score': score, 'Risco': 100 - score}

    return render_template('detalhe_cliente.html', cliente=cliente, info=info, chart_data=chart_data)

@app.route('/editar-cliente/<int:id>', methods=['GET', 'POST'])
@papel_obrigatorio(['gestor', 'admin'])
def editar_cliente(id):
    cliente = db.get_or_404(DimCliente, id)
    info = FactInfoBancaria.query.filter_by(ClienteId=id).first()

    if request.method == 'POST':
        # Atualizar DimCliente
        cliente.Email = request.form.get('email')
        # ... outros campos ...

        # Atualizar ou Criar FactInfoBancaria
        if not info:
            info = FactInfoBancaria(ClienteId=id, Saldo=0, DataRegisto=datetime.now())
            db.session.add(info)
        
        info.EstadoCivil = request.form.get('estado_civil')
        info.EmprestimoCasa = 'emprestimo_casa' in request.form
        info.EmprestimoPessoal = 'emprestimo_pessoal' in request.form
        
        db.session.commit()
        flash('Dados atualizados com sucesso.', 'sucesso')
        return redirect(url_for('detalhe_cliente', id=id))

    return render_template('editar_cliente.html', cliente=cliente, info=info)

@app.route('/eliminar-cliente/<int:id>', methods=['POST'])
@papel_obrigatorio(['gestor', 'admin'])
def eliminar_cliente(id):
    # Nota: Numa base de dados real, cuidado com Foreign Keys (Transações, etc.)
    # Primeiro apagar dependências ou usar cascade delete no modelo
    # Usar SQL puro para apagar transações, contornando o problema do modelo
    sql_transacoes = text("DELETE FROM FactTransacao WHERE ClienteId = :cliente_id")
    db.session.execute(sql_transacoes, {'cliente_id': id})
    FactInfoBancaria.query.filter_by(ClienteId=id).delete()
    DimCliente.query.filter_by(ClienteId=id).delete()
    
    db.session.commit()
    flash('Cliente eliminado.', 'sucesso')
    return redirect(url_for('lista_clientes'))


# --- ROTAS ADMIN (GESTÃO DE GESTORES) ---

@app.route('/lista-gestores', methods=['GET'])
@papel_obrigatorio('admin')
def lista_gestores():
    search_query = request.args.get('q')
    
    if search_query:
        gestores = DimGestor.query.filter(DimGestor.Username.contains(search_query)).all()
    else:
        gestores = DimGestor.query.all()

    return render_template('lista_gestores.html', gestores=gestores)

@app.route('/eliminar-gestor/<int:id>', methods=['POST'])
@papel_obrigatorio('admin')
def eliminar_gestor(id):
    # Cuidado: Verificar se o gestor tem clientes associados antes de apagar
    DimGestor.query.filter_by(GestorId=id).delete()
    db.session.commit()
    flash('Gestor eliminado.', 'sucesso')
    return redirect(url_for('lista_gestores'))

def prever_default(cliente_id):
    """
    Usa o modelo de ML para prever a probabilidade de default de um cliente.
    """
    try:
        artefacts = joblib.load('logit_model_artefacts.joblib')
        model = artefacts['model']
        model_columns = artefacts['model_columns']
    except FileNotFoundError:
        # Se o modelo não for encontrado, não é possível prever.
        # Pode-se retornar um valor neutro ou lançar um erro.
        return None

    cliente = db.session.get(DimCliente, cliente_id)
    info = FactInfoBancaria.query.filter_by(ClienteId=cliente_id).first()

    if not all([cliente, info, cliente.DataNascimento, info.Emprego, info.EstadoCivil, info.Educacao]):
        # Retorna None se faltarem dados essenciais para a previsão.
        return None

    # 1. Preparar os dados para a previsão
    age = (datetime.now().date() - cliente.DataNascimento).days // 365
    
    dados_cliente = pd.DataFrame({
        'age': [age],
        'job': [info.Emprego],
        'marital': [info.EstadoCivil],
        'education': [info.Educacao],
        'balance': [info.Saldo],
        'housing': ['yes' if info.EmprestimoCasa else 'no'],
        'loan': ['yes' if info.EmprestimoPessoal else 'no']
    })

    # 2. One-hot encode dos dados
    dados_cliente_encoded = pd.get_dummies(dados_cliente, drop_first=True, dtype=int)

    # 3. Alinhar colunas com as do modelo (importante para garantir consistência)
    dados_cliente_aligned = dados_cliente_encoded.reindex(columns=model_columns, fill_value=0)

    # 4. Adicionar constante para o modelo statsmodels
    dados_cliente_const = sm.add_constant(dados_cliente_aligned, has_constant='add')

    # 5. Fazer a previsão
    probabilidade = model.predict(dados_cliente_const)
    
    return round(float(probabilidade.iloc[0]), 4)

# --- ROTAS DE EMPRÉSTIMO ---

@app.route('/pedir-emprestimo', methods=['GET', 'POST'])
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def pedir_emprestimo():
    if request.method == 'POST':
        valor = request.form.get('valor')
        tipo_emprestimo = request.form.get('tipo_emprestimo')
        user_id = session['utilizador_id']

        try:
            # Tratar formato de número (ex: 350.000 -> 350000)
            if valor:
                valor = valor.replace('.', '').replace(',', '.')
            valor_float = float(valor)
            if valor_float <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            flash('O valor do empréstimo deve ser um número positivo.', 'perigo')
            return redirect(url_for('pedir_emprestimo'))

        # Correr o modelo para prever a probabilidade de default (incumprimento)
        probabilidade = prever_default(user_id)
        
        if probabilidade is None:
            flash('Não foi possível calcular o risco. Por favor, garanta que todos os seus dados de perfil (emprego, estado civil, educação) estão preenchidos.', 'perigo')
            return redirect(url_for('meu_perfil'))

        limiar_rejeicao = 0.50
        status = ''

        if probabilidade > limiar_rejeicao:
            # Pedido Rejeitado
            status = 'rejeitado'
            flash('O seu pedido de empréstimo foi rejeitado devido a um alto risco de incumprimento.', 'perigo')
        else:
            # Pedido Aprovado
            status = 'aprovado'
            
            # 1. Guardar o empréstimo na nova tabela
            novo_emprestimo = FactEmprestimo(
                ClienteId=user_id,
                Valor=valor_float,
                TipoEmprestimo=tipo_emprestimo,
                DataPedido=datetime.now().date(),
                ProbabilidadeDefault=probabilidade
            )
            db.session.add(novo_emprestimo)
            
            # 2. Atualizar o saldo do cliente
            info_bancaria = FactInfoBancaria.query.filter_by(ClienteId=user_id).first()
            if info_bancaria:
                info_bancaria.Saldo += valor_float
                if tipo_emprestimo == 'pessoal':
                    info_bancaria.EmprestimoPessoal = True
                elif tipo_emprestimo == 'casa':
                    info_bancaria.EmprestimoCasa = True
            
            # 3. Registar a transação na FactTransacao para aparecer nos movimentos
            nova_transacao = FactTransacao(
                ClienteId=user_id,
                Descricao=f"Empréstimo {tipo_emprestimo.capitalize()} Aprovado",
                Categoria=f"Empréstimo {tipo_emprestimo.capitalize()}",
                Quantidade=valor_float,
                DataTransacao=datetime.now().date()
            )
            db.session.add(nova_transacao)
            
            db.session.commit()
            # Formatar valor para PT (ex: 350.000,00)
            valor_formatado = f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            valor_formatado = formatar_numero_pt(valor_float)
            flash(f'Parabéns! O seu empréstimo de €{valor_formatado} foi aprovado e o valor adicionado ao seu saldo.', 'sucesso')

        return redirect(url_for('resultado_emprestimo', status=status, probabilidade=probabilidade))

    return render_template('pedir_emprestimo.html')

@app.route('/resultado-emprestimo')
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def resultado_emprestimo():
    status = request.args.get('status')
    probabilidade = request.args.get('probabilidade', type=float)

    # Define o URL do GIF a ser mostrado com base no estado
    gif_aprovado = 'https://media.tenor.com/FRtgI3P9GCYAAAAM/dive-into-money-money-bin.gif'
    gif_rejeitado = 'https://media.tenor.com/43F34BI9HEQAAAAM/funny-cartoon-wolf.gif'
    
    gif_url = gif_aprovado if status == 'aprovado' else gif_rejeitado

    return render_template('resultado_emprestimo.html', 
                           status=status, 
                           probabilidade=probabilidade,
                           gif_url=gif_url)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)