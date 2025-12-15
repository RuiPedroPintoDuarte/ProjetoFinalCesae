import pandas as pd
import sqlalchemy

from Repository import SQLConnection

tableName = "DimGestor"
engine = SQLConnection.engine

colunas = ["GestorId", "Username", "Email", "PalavraPasse"]

def getGestorTable():
    return pd.read_sql_table(tableName, engine)

def getGestorIds():
    userdf = getGestorTable()
    return userdf["GestorId"].tolist()

def getNextId():
    gestorIds = getGestorIds()
    gestorIds.sort()
    if (len(gestorIds) > 0):
        return gestorIds[-1] + 1
    else:
        return 1

def addGestor(Username, Email, PalavraPasse):
    id = getNextId()
    dadosGestor = [Username, Email, PalavraPasse]
    userdf = pd.DataFrame([[id] + dadosGestor], columns=colunas)
    userdf.to_sql(
        tableName,
        engine,
        if_exists="append",
        index=False
    )
    return id

def alterValue(GestorId, novoValor, campoDoNovoValor):
    with engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(f"""
                UPDATE {tableName}
                SET {campoDoNovoValor} = :nova
                WHERE GestorId = :cid
            """),
            {"nova": novoValor, "cid": GestorId}
        )
        conn.commit()
        return result.rowcount > 0

#addGestor("Gerunbindio", "gerunbindio@gmail.com", "gerundando")