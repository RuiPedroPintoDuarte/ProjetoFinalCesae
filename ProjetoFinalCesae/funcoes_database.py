import pandas as pd
import sqlalchemy

server = 'localhost'
database = 'BankDatabase'

columnsUtilizador = ["UtilizadorId", "Username", "Email", "PalavraPasse", "TipoUtilizador"]
columnsCliente = ["UtilizadorId", "Idade", "Emprego", "EstadoCivil", "Educacao",
                  "DefaultCredit", "Saldo", "EmprestimoCasa", "EmprestimoPessoal",
                  "Contacto", "DiaSemana", "Mes", "Duracao", "NContactos", "pDias",
                  "ContactosPrevios", "pOutcome", "Subscreveu"]

engine = sqlalchemy.create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

def getUtilizadorTable():
    return pd.read_sql_table("Utilizador", engine)

def getClienteTable():
    return pd.read_sql_table("Cliente", engine)

def getGestorAssociadosTable():
    return pd.read_sql_table("GestorAssociados", engine)

def getUtilizadorIds():
    userdf = getUtilizadorTable()
    return userdf["UtilizadorId"].tolist()

def getNextId():
    utilizadorIds = getUtilizadorIds()
    utilizadorIds.sort()
    if (len(utilizadorIds) > 0):
        return utilizadorIds[-1] + 1
    else:
        return 1

def addUtilizador(id, dados_utilizador):
     userdf = pd.DataFrame([[id] + dados_utilizador], columns = columnsUtilizador)
     userdf.to_sql(
         "Utilizador",
         engine,
         if_exists="append",
         index=False
     )

def addCliente(dados_utilizador, dados_cliente):
    id = getNextId()
    addUtilizador(id,dados_utilizador + [1])
    print(dados_cliente)
    df_cliente = pd.DataFrame([[id] + dados_cliente], columns = columnsCliente)
    for i in ["DefaultCredit", "EmprestimoCasa","EmprestimoPessoal", "Subscreveu"]:
        if df_cliente.iloc[0][i] == "yes":
            df_cliente.at[0, i] = 1
        elif df_cliente.iloc[0][i] == "no":
            df_cliente.at[0, i] = 0
    df_cliente.to_sql(
        "Cliente",
        engine,
        if_exists="append",
        index=False
    )

def addAdmin(dados_utilizador):
    addUtilizador(getNextId(), dados_utilizador)

def addGestor(dados_utilizador, lista_clientes):
    id = getNextId()
    addUtilizador(id, dados_utilizador + [1])
    df_gestor = getGestorAssociadosTable()
    new_col = []
    for id in df_gestor["UtilizadorId"]:
        if id in lista_clientes:
            new_col.append(1)
        else:
            new_col.append(0)
    df_gestor.insert(1, id, new_col)
    df_gestor.to_sql(
        "GestoresAssociados",
        engine,
        if_exists="replace",
        index=False
    )
#addCliente(["Claudia", "claudia@gmail.com","claudia123"], [58,"management","married","tertiary","no",2143,"yes","no","unknown",5,"may",261,1,-1,0,"unknown","no"])
