from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from functools import wraps
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/BankDatabase?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
# Em produção, esta chave deve ser carregada de uma variável de ambiente e não estar hardcoded.
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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

# --- ROTAS CLIENTE ---

@app.route('/meus-movimentos')
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def meus_movimentos():
    user_id = session['utilizador_id']
    cliente = DimCliente.query.get(user_id)
    
    # Obter saldo e info bancária
    info_bancaria = FactInfoBancaria.query.filter_by(ClienteId=user_id).first()
    saldo = info_bancaria.Saldo if info_bancaria else 0.0

    # Obter últimas transações (Home do Wireframe)
    transacoes = FactTransacao.query.filter_by(ClienteId=user_id)\
        .order_by(FactTransacao.DataTransacao.desc()).limit(10).all()

    return render_template('cliente_movimentos.html', cliente=cliente, saldo=saldo, transacoes=transacoes)

@app.route('/minha-atividade')
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def minha_atividade():
    user_id = session['utilizador_id']
    
    # Agregação para o gráfico de barras (Total Gasto/Mês)
    # Exemplo: Soma quantidades negativas (gastos) agrupadas por mês
    # NOTA: Agrupar também por ano para não misturar dados de anos diferentes.
    gastos_por_mes = db.session.query(
        func.year(FactTransacao.DataTransacao).label('ano'),
        func.month(FactTransacao.DataTransacao).label('mes'),
        func.sum(FactTransacao.Quantidade).label('total')
    ).filter(
        FactTransacao.ClienteId == user_id,
        FactTransacao.Quantidade < 0  # Apenas gastos
    ).group_by(func.year(FactTransacao.DataTransacao), func.month(FactTransacao.DataTransacao)).order_by('ano', 'mes').all()

    # Passar estes dados para o Chart.js no frontend
    labels = [f"{d.ano}-{d.mes:02d}" for d in gastos_por_mes]
    values = [abs(d.total) for d in gastos_por_mes] # Valor absoluto para o gráfico

    return render_template('cliente_atividade.html', labels=labels, values=values)

@app.route('/meu-perfil')
@autenticacao_obrigatoria
@papel_obrigatorio('cliente')
def meu_perfil():
    user_id = session['utilizador_id']
    cliente = DimCliente.query.get(user_id)
    info = FactInfoBancaria.query.filter_by(ClienteId=user_id).first()
    
    return render_template('cliente_perfil.html', cliente=cliente, info=info)

# --- ROTAS GESTOR / ADMIN (GESTÃO DE CLIENTES) ---

@app.route('/lista-clientes', methods=['GET'])
@papel_obrigatorio(['gestor', 'admin'])
def lista_clientes():
    search_query = request.args.get('q')
    
    if search_query:
        # Pesquisa por nome ou NIF
        clientes = DimCliente.query.filter(
            (DimCliente.Nome.contains(search_query)) | 
            (DimCliente.NIF.contains(search_query))
        ).all()
    else:
        clientes = DimCliente.query.all()

    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/detalhe-cliente/<int:id>')
@papel_obrigatorio(['gestor', 'admin'])
def detalhe_cliente(id):
    cliente = DimCliente.query.get_or_404(id)
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
    cliente = DimCliente.query.get_or_404(id)
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
    FactInfoBancaria.query.filter_by(ClienteId=id).delete()
    FactTransacao.query.filter_by(ClienteId=id).delete()
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)