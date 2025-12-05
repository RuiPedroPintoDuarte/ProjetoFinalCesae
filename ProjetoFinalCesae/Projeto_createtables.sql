CREATE DATABASE BankDatabase;
USE BankDatabase

CREATE TABLE Utilizador(
	UtilizadorId INT,
	Username NVARCHAR(120) NOT NULL,
	Email NVARCHAR(120) NOT NULL,
	PalavraPasse NVARCHAR(120) NOT NULL,
	TipoUtilizador INT NOT NULL
	CONSTRAINT PK_Utilizador PRIMARY KEY (UtilizadorId),
)

CREATE TABLE Cliente(
	UtilizadorId INT,
	Idade INT,
	Emprego NVARCHAR(120),
	EstadoCivil NVARCHAR(120),
	Educacao NVARCHAR(120),
	DefaultCredit BIT,
	Saldo INT,
	EmprestimoCasa BIT,
	EmprestimoPessoal BIT,
	Contacto NVARCHAR(120),
	DiaSemana NVARCHAR(120),
	Mes NVARCHAR(120),
	Duracao INT,
	NContactos INT,
	pDias INT,
	ContactosPrevios INT,
	pOutcome NVARCHAR(120),
	Subscreveu BIT
	CONSTRAINT FK_Utilizador FOREIGN KEY
	(UtilizadorId) REFERENCES dbo.Utilizador(UtilizadorId)
)

CREATE TABLE GestoresAssociados(
	UtilizadorId INT NOT NULL
	CONSTRAINT FK_UtilizadorGestor FOREIGN KEY
	(UtilizadorId) REFERENCES dbo.Utilizador(UtilizadorId)
)

SELECT * FROM dbo.Utilizador
SELECT * FROM dbo.Cliente
SELECT * FROM dbo.GestoresAssociados