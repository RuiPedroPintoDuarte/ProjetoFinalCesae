import pandas as pd

import ClientRepository

tableName = "DimCliente"
engine = ClientRepository.engine


columnsCliente = ["UtilizadorId", "Idade", "Emprego", "EstadoCivil", "Educacao",
                  "DefaultCredit", "Saldo", "EmprestimoCasa", "EmprestimoPessoal",
                  "Contacto", "DiaSemana", "Mes", "Duracao", "NContactos", "pDias",
                  "ContactosPrevios", "pOutcome", "Subscreveu"]

def getClienteTable():
    return pd.read_sql_table(tableName, engine)

def getClienteInfoTable():
    return pd.read_sql_table(tableName, engine)

def getUtilizadorIds():
    userdf = getClienteTable()
    return userdf["ClienteId"].tolist()