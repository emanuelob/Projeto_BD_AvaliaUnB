-- -----------------------------------------------------
-- Tabela estudantes
-- -----------------------------------------------------
CREATE TABLE estudantes (
  `id_estudante` INT NOT NULL AUTO_INCREMENT,
  `matricula_estudante` INT NOT NULL,
  `nome_estudante` VARCHAR(200) NOT NULL,
  `curso_estudante` VARCHAR(50) NOT NULL,
  `email_estudante` VARCHAR(250) NOT NULL,
  `senha_estudante` VARCHAR(30) NOT NULL,
  `cargo_estudante` VARCHAR(30) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `foto_estudante` BLOB NULL,
  UNIQUE INDEX `id_estudante_UNIQUE` (`id_estudante`),
  PRIMARY KEY (`matricula_estudante`),
  UNIQUE INDEX `email_estudante_UNIQUE` (`email_estudante`));

-- -----------------------------------------------------
-- Tabela departamentos
-- -----------------------------------------------------
CREATE TABLE departamentos (
  `cod_departamento` INT NOT NULL,
  `nome_departamento` VARCHAR(300) NOT NULL,
  PRIMARY KEY (`cod_departamento`));

-- -----------------------------------------------------
-- Tabela professores
-- -----------------------------------------------------
CREATE TABLE professores (
  `id_professor` INT NOT NULL AUTO_INCREMENT,
  `matricula_professor` NULL,
  `nome_professor` VARCHAR(200) NOT NULL,
  `email_professor` VARCHAR(250) NULL,
  `cod_departamento` INT NOT NULL,
  PRIMARY KEY (`id_professor`),
  UNIQUE INDEX `matricula_professor_UNIQUE` (`matricula_professor`),
  UNIQUE INDEX `email_professor_UNIQUE` (`email_professor`),
  INDEX `fk_professores_departamentos_idx` (`cod_departamento`),
  CONSTRAINT `fk_professores_departamentos`
    FOREIGN KEY (`cod_departamento`)
    REFERENCES departamentos (`cod_departamento`));

-- -----------------------------------------------------
-- Tabela disciplinas
-- -----------------------------------------------------
CREATE TABLE disciplinas (
  `cod_disciplina` VARCHAR(10) NOT NULL,
  `nome_disciplina` VARCHAR(300) NOT NULL,
  `cod_departamento` INT NOT NULL,
  PRIMARY KEY (`cod_disciplina`),
  INDEX `fk_disciplinas_departamentos1_idx` (`cod_departamento`),
  CONSTRAINT `fk_disciplinas_departamentos1`
    FOREIGN KEY (`cod_departamento`)
    REFERENCES departamentos (`cod_departamento`));

-- -----------------------------------------------------
-- Tabela turmas
-- -----------------------------------------------------
CREATE TABLE turmas (
  `numero_turma` INT NOT NULL,
  `periodo_turma` VARCHAR(10) NOT NULL,
  `id_professor` INT NOT NULL,
  `cod_disciplina` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`numero_turma`, `periodo_turma`, `cod_disciplina`),
  INDEX `fk_turmas_professores1_idx` (`id_professor`),
  INDEX `fk_turmas_disciplinas1_idx` (`cod_disciplina`),
  CONSTRAINT `fk_turmas_professores1`
    FOREIGN KEY (`id_professor`)
    REFERENCES professores (`id_professor`)
  CONSTRAINT `fk_turmas_disciplinas1`
    FOREIGN KEY (`cod_disciplina`)
    REFERENCES disciplinas (`cod_disciplina`));

-- -----------------------------------------------------
-- Tabela avaliacoes
-- -----------------------------------------------------
CREATE TABLE avaliacoes (
  `id_avaliacao` INT NOT NULL AUTO_INCREMENT,
  `matricula_estudante` INT NOT NULL,
  `numero_turma` INT NOT NULL,
  `periodo_turma` VARCHAR(10) NOT NULL,
  `cod_disciplina` VARCHAR(10) NOT NULL,
  `avaliacao` TEXT NOT NULL,
  `nota` DOUBLE NOT NULL,
  PRIMARY KEY (`id_avaliacao`),
  INDEX `fk_avaliacoes_estudantes1_idx` (`matricula_estudante`),
  INDEX `fk_avaliacoes_turmas1_idx` (`numero_turma`, `periodo_turma`, `cod_disciplina`),
  CONSTRAINT `fk_avaliacoes_estudantes1`
    FOREIGN KEY (`matricula_estudante`)
    REFERENCES estudantes (`matricula_estudante`)
  CONSTRAINT `fk_avaliacoes_turmas1`
    FOREIGN KEY (`numero_turma` , `periodo_turma` , `cod_disciplina`)
    REFERENCES turmas (`numero_turma` , `periodo_turma` , `cod_disciplina`));

-- -----------------------------------------------------
-- Tabela denuncias
-- -----------------------------------------------------
CREATE TABLE denuncias (
  `id_denuncias` INT NOT NULL AUTO_INCREMENT,
  `id_avaliacao` INT NOT NULL,
  `matricula_estudante` INT NOT NULL,
  `motivo` TEXT NOT NULL,
  PRIMARY KEY (`id_denuncias`),
  INDEX `fk_denuncias_avaliacoes1_idx` (`id_avaliacao`),
  INDEX `fk_denuncias_estudantes1_idx` (`matricula_estudante`),
  CONSTRAINT `fk_denuncias_avaliacoes1`
    FOREIGN KEY (`id_avaliacao`)
    REFERENCES avaliacoes (`id_avaliacao`)
  CONSTRAINT `fk_denuncias_estudantes1`
    FOREIGN KEY (`matricula_estudante`)
    REFERENCES estudantes (`matricula_estudante`));