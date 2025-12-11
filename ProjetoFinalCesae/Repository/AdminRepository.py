import pandas as pd

import SQLConnection

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

addAdmin("GerunbindioAdmin", "gerunbindio@gmail.com", "gerundando")