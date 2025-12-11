import pandas as pd

from Repository import SQLConnection

tableName = "FactGestorCliente"
engine = SQLConnection.engine

colunas = ["GestorId", "ClienteId"]

def getInfoTable():
    return pd.read_sql_table(tableName, engine)

def addClienteInfo(GestorId, ListClienteIds):
    dadosCliente = []
    for ClienteId in ListClienteIds:
        dadosCliente.append([GestorId, ClienteId])
    userdf = pd.DataFrame(dadosCliente, columns=colunas)
    userdf.to_sql(
        tableName,
        engine,
        if_exists="append",
        index=False
    )
    return id

#addClienteInfo(1, [1,2])