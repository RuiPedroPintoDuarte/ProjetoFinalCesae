import pandas as pd
import os
import random
import string
import datetime

import Repository

tableName = "DimCliente"
engine = Repository.SQLConnection.engine

colunas = ["ClienteId", "Emprego", "EstadoCivil", "Educacao", "DefaultCredit", "Saldo",
           "EmprestimoCasa", "EmprestimoPessoal", "DataRegisto"]
colunas2 = ["ClienteId", "Nome", "DataNascimento", "NIF", "Username", "Email", "PalavraPasse"]
pathFile = os.getcwd() + "\\bank-full.csv"

def createClienteTable():
    df = pd.read_csv(pathFile, delimiter=";")
    print(df.columns)
    df["housing"] = df["housing"].apply(lambda x: 1 if x == 'yes' else 0)
    df["loan"] = df["loan"].apply(lambda x: 1 if x == 'yes' else 0)
    df["default"] = df["loan"].apply(lambda x: 1 if x == 'yes' else 0)
    print(df)
    new_df = []
    new_df_2 = []
    for i in range(len(df)):
        print(i)
        data = getDataNascimento(df["age"][i])
        letters = string.ascii_lowercase
        username = ''.join(random.choice(letters) for i in range(8))
        email = username + "@gmail.com"
        password = username + "123"
        date =  "2025-" + str(df["month"][i]) + "-" + str(df["day"][i])
        #id = Repository.ClientRepository.addCliente(username, data, random.randint(100000000, 999999999), username, email, password)
        #Repository.ClienteInfoRepository.addClienteInfo(id, df["job"][i], df["marital"][i], df["education"][i], df["default"][i],
                                             #df["balance"][i], df["housing"][i], df["loan"][i], date)
        new_df_2.append([i, username, data, random.randint(100000000, 999999999), username, email, password])
        new_df.append([i, df["job"][i], df["marital"][i], df["education"][i], df["default"][i],
                                             df["balance"][i], df["housing"][i], df["loan"][i], date])
    new_df_2 = pd.DataFrame(new_df_2, columns = colunas2)
    new_df_2.to_sql(
        tableName,
        engine,
        if_exists="append",
        index=False
    )
    new_df = pd.DataFrame(new_df, columns=colunas)
    new_df.to_sql(
        "FactInfoBancaria",
        engine,
        if_exists="append",
        index=False
    )




def getDataNascimento(idade):
    dia = str(random.randint(1, 12))
    mes = str(random.randint(1, 12))
    ano = str(datetime.datetime.now().year - idade)
    return ano + "-" + mes + "-" + dia

createClienteTable()