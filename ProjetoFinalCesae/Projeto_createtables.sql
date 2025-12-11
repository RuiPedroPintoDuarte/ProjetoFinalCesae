CREATE DATABASE BankDatabase;
USE BankDatabase

CREATE TABLE DimCliente(
	ClienteId INT,
	Nome NVARCHAR(120),
	DataNascimento DATE,
	NIF INT,
	Username NVARCHAR(120),
	Email NVARCHAR(120),
	PalavraPasse NVARCHAR(120),
	CONSTRAINT PK_DimCliente PRIMARY KEY (ClienteId),
)

CREATE TABLE DimGestor(
	GestorId INT,
	Username NVARCHAR(120),
	Email NVARCHAR(120),
	PalavraPasse NVARCHAR(120),
	CONSTRAINT PK_DimGestor PRIMARY KEY (GestorId),
)

CREATE TABLE DimAdmin(
	AdminId INT,
	Username NVARCHAR(120),
	Email NVARCHAR(120),
	PalavraPasse NVARCHAR(120),
	CONSTRAINT PK_DimAdmin PRIMARY KEY (AdminId),
)

CREATE TABLE FactInfoBancaria(
	ClienteId INT,
	Emprego NVARCHAR(120),
	EstadoCivil NVARCHAR(120),
	Educacao NVARCHAR(120),
	DefaultCredit BIT,
	Saldo INT,
	EmprestimoCasa BIT,
	EmprestimoPessoal BIT,
	DataRegisto DATE,
	CONSTRAINT FK_ClienteInfo FOREIGN KEY
	(ClienteId) REFERENCES dbo.DimCliente(ClienteId)
)

CREATE TABLE FactGestorCliente(
	GestorId INT,
	ClienteId INT,
	CONSTRAINT FK_Gestor FOREIGN KEY
	(GestorId) REFERENCES dbo.DimGestor(GestorId),
	CONSTRAINT FK_Cliente FOREIGN KEY
	(ClienteId) REFERENCES dbo.DimCliente(ClienteId)
)

CREATE TABLE FactTransacao(
    TransacaoId INT IDENTITY(1,1) PRIMARY KEY, 
    ClienteId INT,
    Descricao VARCHAR(120),
    Quantidade INT,
    DataTransacao DATE,
    Categoria VARCHAR(120),
    CONSTRAINT FK_ClienteTransacao FOREIGN KEY
    (ClienteId) REFERENCES dbo.DimCliente(ClienteId)
)

INSERT INTO DimAdmin (AdminId, Username, Email, PalavraPasse)
VALUES (1, 'admin_geral', 'admin@bankdatabase.com', 'adminPass123');

INSERT INTO DimGestor (GestorId, Username, Email, PalavraPasse)
VALUES (101, 'joao_gestor', 'joao.gestor@bankdatabase.com', 'gestorPass123');

INSERT INTO FactGestorCliente (GestorId, ClienteId)
VALUES
(101, 1), 
(101, 2), 
(101, 3); 


SELECT * FROM dbo.DimCliente
SELECT * FROM dbo.DimGestor
SELECT * FROM dbo.DimAdmin
SELECT * FROM dbo.FactInfoBancaria
SELECT * FROM dbo.FactGestorCliente
SELECT * FROM dbo.FactTransacao