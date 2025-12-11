import sqlalchemy

server = 'localhost'
database = 'BankDatabase'

engine = sqlalchemy.create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)
