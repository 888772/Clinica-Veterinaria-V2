create database clinica_veterianria;
use clinica_veterianria;

create table Cliente(
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Endereco VARCHAR(255),
    Telefone VARCHAR(20),
    Email VARCHAR(100),
    CPF VARCHAR(20) UNIQUE
);

create table Pet(
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Data_Nascimento DATE,
    Especie VARCHAR(100) NOT NULL, -- TRATAR NO CÓDIGIO
    ID_Cliente INT,
    FOREIGN KEY (ID_Cliente)
    REFERENCES Cliente(ID)
);

create table Vacina(
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Marca VARCHAR(255) NOT NULL,
    Tipo VARCHAR(255) NOT NULL,
    ID_Pet INT,
    FOREIGN KEY (ID_Pet)
    REFERENCES Pet(ID)
);

create table Veterinario(
	ID INT PRIMARY KEY AUTO_INCREMENT,
    CRMV VARCHAR(20) UNIQUE NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    Especialidade VARCHAR(100) NOT NULL,
    Telefone VARCHAR(20),
    Email VARCHAR(100)
);

create table Consulta(
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Data_Consulta DATE NOT NULL,
    Horas TIME NOT NULL,
    Observacoes VARCHAR(100),
    Valor FLOAT,
    Status_Consulta ENUM('CONCLUIDA', 'EM ANDAMENTO', 'RESERVADA') NOT NULL,
    ID_Pet INT,
    CRMV VARCHAR(20),
    FOREIGN KEY (ID_Pet)
    REFERENCES Pet(ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    
    FOREIGN KEY (CRMV)
	REFERENCES Veterinario(CRMV)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

