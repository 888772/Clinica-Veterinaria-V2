-- UPDATES

UPDATE Cliente
SET Telefone = '11999998888'
WHERE ID = 1;

UPDATE Veterinario
SET Especialidade = 'Clínico Geral'
WHERE ID = 3;

UPDATE Consulta
SET Status_Consulta = 'CONCLUIDA'
WHERE ID = 6;

UPDATE Pet
SET Especie = 'Indefinida'
WHERE ID = 9;

UPDATE Consulta
SET Valor = 180.00
WHERE ID = 2;

-- DELETES

DELETE FROM Pet
WHERE ID = 6;

DELETE FROM Vacina
WHERE ID = 10;

DELETE FROM Consulta
WHERE Status_Consulta = 'RESERVADA'
AND ID = 8;

DELETE FROM Cliente
WHERE ID = 10;

DELETE FROM Vacina
WHERE Tipo = 'V8'
AND ID_Pet = 5;

-- SELECT

SELECT P.Nome AS Pet, C.Nome AS Cliente
FROM Pet P
JOIN Cliente C ON P.ID_Cliente = C.ID;

SELECT 
    P.Nome AS Pet,
    V.Nome AS Veterinario,
    C.Data_Consulta,
    C.Status_Consulta
FROM Consulta C
JOIN Pet P ON C.ID_Pet = P.ID
JOIN Veterinario V ON C.ID_Veterinario = V.ID;

SELECT 
    P.Nome AS Pet,
    Vc.Tipo AS Vacina,
    Vc.Marca
FROM Vacina Vc
JOIN Pet P ON Vc.ID_Pet = P.ID;

SELECT 
    P.Nome AS Pet,
    C.Data_Consulta,
    C.Valor
FROM Consulta C
JOIN Pet P ON C.ID_Pet = P.ID
WHERE C.Status_Consulta = 'CONCLUIDA';

SELECT 
    V.Nome,
    COUNT(C.ID) AS Total_Consultas
FROM Veterinario V
LEFT JOIN Consulta C ON V.ID = C.ID_Veterinario
GROUP BY V.Nome;
