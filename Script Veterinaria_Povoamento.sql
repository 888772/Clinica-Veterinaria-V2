use clinica_veterianria;

-- TABELA CLIENTE

INSERT INTO Cliente (Nome, Endereco, Telefone, Email, CPF) VALUES
('Ana Silva', 'Rua A, 100', '11999990001', 'ana@email.com', '111.111.111-01'),
('Bruno Costa', 'Rua B, 200', '11999990002', 'bruno@email.com', '111.111.111-02'),
('Carla Souza', 'Rua C, 300', '11999990003', 'carla@email.com', '111.111.111-03'),
('Daniel Lima', 'Rua D, 400', '11999990004', 'daniel@email.com', '111.111.111-04'),
('Eduarda Rocha', 'Rua E, 500', '11999990005', 'eduarda@email.com', '111.111.111-05'),
('Felipe Alves', 'Rua F, 600', '11999990006', 'felipe@email.com', '111.111.111-06'),
('Gabriela Torres', 'Rua G, 700', '11999990007', 'gabi@email.com', '111.111.111-07'),
('Henrique Melo', 'Rua H, 800', '11999990008', 'henrique@email.com', '111.111.111-08'),
('Isabela Nunes', 'Rua I, 900', '11999990009', 'isa@email.com', '111.111.111-09'),
('João Pereira', 'Rua J, 1000', '11999990010', 'joao@email.com', '111.111.111-10');

-- TABELA PET

INSERT INTO Pet (Nome, Data_Nascimento, Especie, ID_Cliente) VALUES
('Rex', '2018-05-10', 'Cachorro', 1),
('Mia', '2019-07-12', 'Gato', 2),
('Thor', '2020-01-20', 'Cachorro', 3),
('Luna', '2017-09-15', 'Gato', 4),
('Bob', '2016-03-22', 'Cachorro', 5),
('Nina', '2021-06-30', 'Ave', 6),
('Max', '2018-11-05', 'Cachorro', 7),
('Mel', '2019-08-08', 'Gato', 8),
('Paco', '2020-02-14', 'Ave', 9),
('Toby', '2015-12-01', 'Cachorro', 10);

-- TABELA VETERINARIO

INSERT INTO Veterinario (CRMV, Nome, Especialidade, Telefone, Email) VALUES
('CRMV001', 'Dr. Carlos', 'Clínico Geral', '11988880001', 'carlos@vet.com'),
('CRMV002', 'Dra. Paula', 'Dermatologia', '11988880002', 'paula@vet.com'),
('CRMV003', 'Dr. Marcos', 'Ortopedia', '11988880003', 'marcos@vet.com'),
('CRMV004', 'Dra. Fernanda', 'Oftalmologia', '11988880004', 'fernanda@vet.com'),
('CRMV005', 'Dr. Renato', 'Cardiologia', '11988880005', 'renato@vet.com'),
('CRMV006', 'Dra. Aline', 'Clínico Geral', '11988880006', 'aline@vet.com'),
('CRMV007', 'Dr. Tiago', 'Cirurgia', '11988880007', 'tiago@vet.com'),
('CRMV008', 'Dra. Juliana', 'Endocrinologia', '11988880008', 'juliana@vet.com'),
('CRMV009', 'Dr. Pedro', 'Neurologia', '11988880009', 'pedro@vet.com'),
('CRMV010', 'Dra. Camila', 'Clínico Geral', '11988880010', 'camila@vet.com');

-- TABELA CONSULTA

INSERT INTO Consulta
(Data_Consulta, Horas, Observacoes, Valor, Status_Consulta, ID_Pet, CRMV)
VALUES
('2025-01-10', '09:00:00', 'Consulta de rotina', 150.00, 'CONCLUIDA', 1, 'CRMV001'),
('2025-01-11', '10:00:00', 'Vacinação anual', 120.00, 'CONCLUIDA', 2, 'CRMV002'),
('2025-01-12', '11:00:00', 'Exame ortopédico', 200.00, 'CONCLUIDA', 3, 'CRMV003'),
('2025-01-13', '14:00:00', 'Consulta dermatológica', 180.00, 'CONCLUIDA', 4, 'CRMV002'),
('2025-01-14', '15:00:00', 'Check-up geral', 150.00, 'CONCLUIDA', 5, 'CRMV001'),
('2025-01-15', '16:00:00', 'Avaliação cirúrgica', 250.00, 'RESERVADA', 6, 'CRMV007'),
('2025-01-16', '09:30:00', 'Consulta geral', 150.00, 'EM ANDAMENTO', 7, 'CRMV006'),
('2025-01-17', '10:30:00', 'Exame cardiológico', 220.00, 'RESERVADA', 8, 'CRMV005'),
('2025-01-18', '11:30:00', 'Avaliação neurológica', 300.00, 'RESERVADA', 9, 'CRMV009'),
('2025-01-19', '13:30:00', 'Consulta de rotina', 150.00, 'CONCLUIDA', 10, 'CRMV010');


-- TABELA VACINA

INSERT INTO Vacina (Marca, Tipo, ID_Pet) VALUES
('Zoetis', 'Antirrábica', 1),
('MSD', 'V8', 2),
('Zoetis', 'V10', 3),
('MSD', 'Antirrábica', 4),
('Virbac', 'V8', 5),
('Virbac', 'Gripe Aviária', 6),
('Zoetis', 'V10', 7),
('MSD', 'V8', 8),
('Virbac', 'Gripe Aviária', 9),
('Zoetis', 'Antirrábica', 10);
