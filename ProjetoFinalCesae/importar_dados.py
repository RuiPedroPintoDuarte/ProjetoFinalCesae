import pandas as pd
import sqlalchemy
import random
import string

from funcoes_database import addCliente

pathFile = "C://Users//User//Downloads//bank+marketing//bank//bank-full.csv"

server = 'localhost'
database = 'BankDatabase'

engine = sqlalchemy.create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

columns = ["UtilizadorId", "Idade", "Emprego", "EstadoCivil", "Educacao",
                  "DefaultCredit", "Saldo", "EmprestimoCasa", "EmprestimoPessoal",
                  "Contacto", "DiaSemana", "Mes", "Duracao", "NContactos", "pDias",
                  "ContactosPrevios", "pOutcome", "Subscreveu"]

columnsUtilizador = ["UtilizadorId", "Username", "Email", "PalavraPasse", "TipoUtilizador"]

'''
def createUtilizadorTable():
    df = pd.read_csv("C://Users//User//Downloads//Churn_Modelling.csv")
    passwords = df['Surname'] + "123"
    emails = df['Surname'].str.lower( ) + "@gmail.com"
    client_type = [1] * len(emails)
    data_users = {"UtilizadorId": df['CustomerId'], "Username": df['Surname'], "Email": emails, "PalavraPasse": passwords, "TipoUtilizador": client_type}
    df_users = pd.DataFrame(data_users)
    df_users.to_sql(
        "Utilizador",
        engine,
        if_exists="append",
        index=False
    )
'''

def createClienteTable():
    df = pd.read_csv(pathFile, delimiter=";")
    for i in range(len(df)):
        letters = string.ascii_lowercase
        username = ''.join(random.choice(letters) for i in range(8))
        email = username + "@gmail.com"
        password = username + "123"
        addCliente([username, email, password], list(df.iloc[i]))

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