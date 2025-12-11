import pandas as pd

import SQLConnection

tableName = "DimCliente"
engine = SQLConnection.engine

colunas = ["ClienteId", "Nome", "DataNascimento", "NIF", "Username", "Email", "PalavraPasse"]

def getClienteTable():
    return pd.read_sql_table(tableName, engine)

def getClienteIds():
    userdf = getClienteTable()
    return userdf["ClienteId"].tolist()

def getNextId():
    clienteIds = getClienteIds()
    clienteIds.sort()
    if (len(clienteIds) > 0):
        return clienteIds[-1] + 1
    else:
        return 1

def addCliente(Nome, DataNascimento, NIF, Username, Email, PalavraPasse):
    id = getNextId()
    dadosCliente = [Nome, DataNascimento, NIF, Username, Email, PalavraPasse]
    userdf = pd.DataFrame([[id] + dadosCliente], columns=colunas)
    userdf.to_sql(
        tableName,
        engine,
        if_exists="append",
        index=False
    )
    return id

addCliente("Ano", "2002-07-29", 234577888, "Boy", "gir@gmail", "ghas")