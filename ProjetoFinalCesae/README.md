# 🏦 Sistema Bancário Inteligente com IA

Bem-vindo ao nosso projeto final! Esta é uma aplicação web completa que simula um sistema bancário moderno. O grande diferencial deste projeto é a integração de **Machine Learning** para auxiliar gestores na tomada de decisão sobre concessão de crédito.

A aplicação não serve apenas para "guardar dados"; ela usa dados históricos para prever o futuro financeiro dos clientes.

---

## 🚀 O que a aplicação faz?

O sistema está dividido em três perfis de utilizador, cada um com uma visão diferente:

### 1. O Cliente 👤
É a visão do utilizador comum do banco.
*   **Consultar Saldo e Movimentos:** Vê o histórico de transações recentes.
*   **Análise de Gastos:** Através de gráficos interativos, o cliente percebe onde gasta mais dinheiro (por categoria e ao longo do tempo).
*   **Perfil:** Visualiza os seus dados pessoais e bancários.

### 2. O Gestor de Conta 💼
É o profissional que gere a relação com os clientes.
*   **Carteira de Clientes:** Acede à lista de clientes que gere.
*   **Simulador de Crédito com IA:** Esta é a "joia da coroa". Ao entrar no detalhe de um cliente, o gestor pode simular um empréstimo. O sistema utiliza um modelo de Inteligência Artificial para calcular, em tempo real, a **probabilidade de incumprimento (default)** desse cliente, ajudando o gestor a decidir se aprova ou não o crédito.
*   **Edição de Dados:** Pode atualizar informações dos clientes.

### 3. O Administrador 🛡️
É o super-utilizador do sistema.
*   **Gestão Total:** Tem todas as permissões dos gestores.
*   **Gestão de Equipa:** Pode criar e eliminar contas de Gestores e outros Administradores.

---

## 🧠 A Inteligência Artificial (Machine Learning)

O sistema utiliza um modelo de **Regressão Logística** treinado com dados históricos reais (`bank-full.csv`).

**Como funciona a previsão?**
Quando um gestor simula um empréstimo, o sistema recolhe dados do cliente (idade, emprego, estado civil, educação, saldo atual, se tem casa própria, etc.) e combina com o valor do empréstimo simulado.

O modelo matemático analisa estes fatores e devolve uma percentagem de risco. Se o risco for elevado, o sistema alerta visualmente o gestor.

---

## 🛠️ Tecnologias Usadas

*   **Backend:** Python com **Flask** (Framework Web).
*   **Base de Dados:** SQL Server (com estrutura Data Warehouse: Tabelas de Factos e Dimensões).
*   **ORM:** SQLAlchemy (para interagir com a base de dados de forma segura).
*   **Data Science:** Pandas, NumPy, Scikit-learn e Statsmodels.
*   **Frontend:** HTML, CSS (Bootstrap) e Chart.js para os gráficos.

---

## ⚙️ Como Instalar e Executar

Siga estes passos para colocar o projeto a rodar na sua máquina:

### 1. Pré-requisitos
*   Python instalado (versão 3.10 ou superior recomendada).
*   SQL Server instalado e a correr localmente.
*   ODBC Driver 17 for SQL Server.

### 2. Configurar a Base de Dados
Certifique-se que tem uma base de dados vazia chamada `BankDatabase` no seu SQL Server local. A aplicação irá criar as tabelas automaticamente, mas a base de dados deve existir.

### 3. Instalar Dependências
Abra o terminal na pasta do projeto e execute:
```bash
pip install -r requirements.txt
```

### 4. Treinar o Modelo de IA
Antes de iniciar o site, precisamos de criar o "cérebro" da IA. Execute o script de treino:
```bash
python treinar_modelo.py
```
*Isto irá gerar um ficheiro `logit_model_artefacts.joblib` que contém o modelo treinado.*

### 5. Povoar a Base de Dados (Opcional, mas recomendado)
Para não começar com o banco vazio, execute o script que importa dados fictícios e cria utilizadores de teste:
```bash
python importar_dados.py
```
*Nota: Este script lê o ficheiro `bank-full.csv` e insere clientes e transações na base de dados.*

### 6. Iniciar a Aplicação
Finalmente, inicie o servidor web:
```bash
python main.py
```
Aceda no seu browser a: `http://127.0.0.1:5000`

---

## 🔑 Credenciais de Acesso (Geradas pelo Importador)

Se correu o script `importar_dados.py`, pode usar estas contas para testar:

**Administrador:**
*   **Email:** `admin@bankdatabase.com`
*   **Password:** `adminPass123`

**Gestor:**
*   **Email:** `joao.gestor@bankdatabase.com`
*   **Password:** `gestorPass123`

**Clientes:**
*   Os clientes são gerados aleatoriamente. Verifique a tabela `DimCliente` na base de dados ou crie um novo registo na página de Login/Registo.