import pandas as pd
import sqlalchemy
import pyodbc

server = 'localhost'
database = 'BankDatabase'

engine = sqlalchemy.create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

def createUtilizadorTable():
    df = pd.read_csv("C://Users//User//Downloads//Churn_Modelling.csv")
    passwords = df['Surname'] + "123"
    emails = df['Surname'].str.lower( ) + "@gmail.com"
    client_type = [1] * len(emails)
    data_users = {"UtilizadorId": df['CustomerId'], "Username": df['Surname'], "Email": emails, "PalavraPasse": passwords, "TipoUtilizador": client_type}
    df_users = pd.DataFrame(data_users)
    print(df_users)
    df_users.to_sql(
        "Utilizador",
        engine,
        if_exists="append",
        index=False
    )

def createClienteTable():
    df = pd.read_csv("C://Users//User//Downloads//Churn_Modelling.csv")
    df = df.drop(columns=['RowNumber'])
    df.columns = ["UtilizadorId", "Apelido", "CreditScore", "Geografia", "Sexo", "Idade",
                  "Tenure", "Saldo", "NumDeProdutos", "TemCartaoCredito", "MembroAtivo",
                  "SalarioEstimado", "Saiu"]
    df.to_sql(
        "Cliente",
        engine,
        if_exists="append",
        index=False
    )
createUtilizadorTable()
createClienteTable()