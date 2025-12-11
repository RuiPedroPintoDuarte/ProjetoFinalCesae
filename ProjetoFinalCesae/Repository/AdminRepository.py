import pandas as pd
import sqlalchemy

from Repository import SQLConnection

tableName = "DimAdmin"
engine = SQLConnection.engine

colunas = ["AdminId", "Username", "Email", "PalavraPasse"]

def getAdminTable():
    return pd.read_sql_table(tableName, engine)

def getAdminIds():
    userdf = getAdminTable()
    return userdf["AdminId"].tolist()

def getNextId():
    adminIds = getAdminIds()
    adminIds.sort()
    if (len(adminIds) > 0):
        return adminIds[-1] + 1
    else:
        return 1

def addAdmin(Username, Email, PalavraPasse):
    id = getNextId()
    dadosAdmin = [Username, Email, PalavraPasse]
    userdf = pd.DataFrame([[id] + dadosAdmin], columns=colunas)
    userdf.to_sql(
        tableName,
        engine,
        if_exists="append",
        index=False
    )
    return id

def alterValue(AdminId, novoValor, campoDoNovoValor):
    with engine.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(f"""
                UPDATE {tableName}
                SET {campoDoNovoValor} = :nova
                WHERE AdminId = :cid
            """),
            {"nova": novoValor, "cid": AdminId}
        )
        conn.commit()
        return result.rowcount > 0

addAdmin("GerunbindioAdmin", "gerunbindio@gmail.com", "gerundando")