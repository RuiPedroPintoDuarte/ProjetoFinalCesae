import pandas as pd

import SQLConnection

tableName = "FactInfoBancaria"
engine = SQLConnection.engine

colunas = ["ClienteId", "Emprego", "EstadoCivil", "Educacao", "DefaultCredit", "Saldo",
           "EmprestimoCasa", "EmprestimoPessoal", "DataRegisto"]

def getInfoTable():
    return pd.read_sql_table(tableName, engine)

def addClienteInfo(ClienteId, Emprego, EstadoCivil, Educacao, DefaultCredit, Saldo,
           EmprestimoCasa, EmprestimoPessoal, DataRegisto):
    dadosCliente = [ClienteId, Emprego, EstadoCivil, Educacao, DefaultCredit, Saldo,
           EmprestimoCasa, EmprestimoPessoal, DataRegisto]
    userdf = pd.DataFrame([dadosCliente], columns=colunas)
    userdf.to_sql(
        tableName,
        engine,
        if_exists="append",
        index=False
    )
    return id