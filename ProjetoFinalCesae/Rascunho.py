import pandas as pd
import os
import random
import string
import datetime

import Repository.SQLConnection as SQLConnection
import Repository.ClientRepository as ClientRepository
import Repository.ClienteInfoRepository as ClienteInfoRepository

tableName = "DimCliente"
engine = SQLConnection.engine

colunas = ["ClienteId", "Nome", "DataNascimento", "NIF", "Username", "Email", "PalavraPasse"]

pathFile = os.getcwd() + "//bank-full.csv"

def createClienteTable():
    df = pd.read_csv(pathFile, delimiter=";")
    for i in range(len(df)):
        data = getDataNascimento(df["Idade"][i])
        letters = string.ascii_lowercase
        username = ''.join(random.choice(letters) for i in range(8))
        email = username + "@gmail.com"
        password = username + "123"
        id = ClientRepository.addCliente(username, data, random.randint(100000000, 999999999), username, email, password, list(df.iloc[i]))
        ClienteInfoRepository.addClienteInfo()



def getDataNascimento(idade):
    dia = random.randint(1, 12)
    mes = random.randint(1, 12)
    ano = datetime.datetime.now().year - idade
    return ano + "-" + mes + "-" + dia