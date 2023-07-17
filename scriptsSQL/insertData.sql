INSERT INTO estudantes (matricula_estudante, nome_estudante, curso_estudante, email_estudante, senha_estudante, cargo_estudante)
VALUES
(123456789, 'Emanuel', 'CiC', 'emanuel@example.com', 'senha1', 'Comum'),
(987654321, 'Chefiaestudantes', 'Eng Elétrica', 'admin@example.com', 'senha2', 'Admin');

INSERT INTO departamentos (cod_departamento, nome_departamento)
VALUES
(359, 'Departamento de Ciência da Computação'),
(008, 'Departamento de Antropologia');

INSERT INTO professores (id_professor, matricula_professor, nome_professor, email_professor, cod_departamento)
VALUES
(1, 189515313, 'Pedro Garcia', 'pedro.garcia@unb.br', 359),
(2, 054648651, 'Andreia de Souza Lobo', 008);

INSERT INTO disciplinas (cod_disciplina, nome_disciplina, cod_departamento)
VALUES
('CIC0003', 'Algoritmo e Programação de Computadores', 359),
('DAN0022', 'Introdução à Antrologia', 643);

INSERT INTO turmas (numero_turma, periodo_turma, id_professor, cod_disciplina)
VALUES
(1, '2023.1', 1, 'CIC0003'),
(1, '2023.1', 2, 'DAN0022');

INSERT INTO avaliacoes (id_avaliacao, matricula_estudante, numero_turma, periodo_turma, cod_disciplina, avaliacao, nota)
VALUES
(1, 123456789, 1, '2023.1', 'CIC0003', 'Garoto de programa.', 5.0),
(2, 987654321, 1, '2023.1', 'DAN0022', 'É tanto debate que não cabe em um cartaz.', 4.0);

INSERT INTO denuncias (id_denuncias, id_avaliacao, matricula_estudante, motivo)
VALUES
(1, 1, 123456789, 'Linguagem Imprópria.'),
(2, 2, 987654321, 'Ofensivo.');
