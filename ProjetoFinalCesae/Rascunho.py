import pandas as pd
import sqlalchemy
import random
import string
import os
import datetime

pathFile = os.getcwd() + "//bank-full.csv"

server = 'localhost'
database = 'BankDatabase'

engine = sqlalchemy.create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

first_names = [
    "Lucas", "Sofia", "Daniel", "Mia", "Gabriel",
    "Olivia", "Leonardo", "Emma", "Matheus", "Isabella",
    "Bruno", "Laura", "Rafael", "Camila", "Henrique",
    "Beatriz", "Felipe", "Mariana", "Thiago", "Clara"
]

surnames = [
    "Almeida", "Martins", "Costa", "Santos", "Ferreira",
    "Rocha", "Carvalho", "Ribeiro", "Oliveira", "Sousa",
    "Teixeira", "Mendes", "Barros", "Azevedo", "Duarte",
    "Nogueira", "Correia", "Pinto", "Moreira", "Lopes"
]

def createClienteTable():
    df = pd.read_csv(pathFile, delimiter=";")
    
    dim_cliente_list = []
    fact_info_list = []
    
    for i in range(len(df)):
        # Dados para DimCliente
        cliente_id = i + 1
        nome_proprio = random.choice(first_names)
        apelido = random.choice(surnames)
        nome = f"{nome_proprio} {apelido}"
        
        idade = int(df["age"][i])
        ano_nasc = datetime.datetime.now().year - idade
        data_nascimento = f"{ano_nasc}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        
        nif = random.randint(100000000, 999999999)
        username = f"{nome_proprio.lower()}{random.randint(1,9999)}"
        email = f"{username}@gmail.com"
        palavra_passe = f"{username}123"
        
        dim_cliente_list.append([cliente_id, nome, data_nascimento, nif, username, email, palavra_passe])
        
        # Dados para FactInfoBancaria
        default_credit = 1 if df["default"][i] == 'yes' else 0
        emprestimo_casa = 1 if df["housing"][i] == 'yes' else 0
        emprestimo_pessoal = 1 if df["loan"][i] == 'yes' else 0
        data_registo = f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        
        fact_info_list.append([cliente_id, df["job"][i], df["marital"][i], df["education"][i], default_credit, df["balance"][i], emprestimo_casa, emprestimo_pessoal, data_registo])

    pd.DataFrame(dim_cliente_list, columns=["ClienteId", "Nome", "DataNascimento", "NIF", "Username", "Email", "PalavraPasse"]).to_sql("DimCliente", engine, if_exists="append", index=False)
    pd.DataFrame(fact_info_list, columns=["ClienteId", "Emprego", "EstadoCivil", "Educacao", "DefaultCredit", "Saldo", "EmprestimoCasa", "EmprestimoPessoal", "DataRegisto"]).to_sql("FactInfoBancaria", engine, if_exists="append", index=False)
    
    print("Dados inseridos com sucesso!")

def createGestorAssociadoTable():
    df = pd.read_csv("C://Users//User//Downloads//Churn_Modelling.csv")
    data_gestor = {"UtilizadorId": df['CustomerId']}
    df_gestor = pd.DataFrame(data_gestor)
    df_gestor.to_sql(
        "GestorAssociados",
        engine,
        if_exists="append",
        index=False
    )

#createUtilizadorTable()
createClienteTable()
#createGestorAssociadoTable()