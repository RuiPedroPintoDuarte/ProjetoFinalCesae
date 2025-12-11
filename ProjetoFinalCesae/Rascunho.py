import pandas as pd
import os
import random
import string
import datetime

import Repository

tableName = "DimCliente"
engine = Repository.SQLConnection.engine

first_names = [
    "Lucas", "Sofia", "Daniel", "Mia", "Gabriel",
    "Olivia", "Leonardo", "Emma", "Matheus", "Isabella",
    "Bruno", "Laura", "Rafael", "Camila", "Henrique",
    "Beatriz", "Felipe", "Mariana", "Thiago", "Clara"
]

surnames = [
    "Almeida", "Martins", "Costa", "Santos", "Ferreira",
    "Rocha", "Carvalho", "Ribeiro", "Oliveira", "Sousa",
    "Teixeira", "Mendes", "Barros", "Azevedo", "Duarte",
    "Nogueira", "Correia", "Pinto", "Moreira", "Lopes"
]

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
    new_df = []
    new_df_2 = []
    for i in range(len(df)):
        data = getDataNascimento(df["age"][i])
        letters = string.ascii_lowercase
        nomeproprio = first_names[random.randint(0, len(first_names)-1)]
        username = nomeproprio + str(random.randint(1,200))
        name = nomeproprio + " " + surnames[random.randint(0, len(surnames)-1)]
        email = username.lower() + "@gmail.com"
        password = username + "123"
        date =  "2025-" + str(df["month"][i]) + "-" + str(df["day"][i])
        #id = Repository.ClientRepository.addCliente(username, data, random.randint(100000000, 999999999), username, email, password)
        #Repository.ClienteInfoRepository.addClienteInfo(id, df["job"][i], df["marital"][i], df["education"][i], df["default"][i],
                                             #df["balance"][i], df["housing"][i], df["loan"][i], date)
        new_df_2.append([i, name, data, random.randint(100000000, 999999999), username, email, password])
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