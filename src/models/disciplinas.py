import mysql.connector

class Disciplina:
    def __init__(self, cod_disciplina, nome_disciplina, cod_departamento):
        self.cod_disciplina = cod_disciplina
        self.nome_disciplina = nome_disciplina
        self.cod_departamento = cod_departamento

class DisciplinaDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT cod_disciplina, nome_disciplina, cod_departamento FROM disciplinas"
            cursor.execute(query)

            disciplinas = []
            for row in cursor.fetchall():
                cod_disciplina, nome_disciplina, cod_departamento = row
                disciplina = Disciplina(cod_disciplina, nome_disciplina, cod_departamento)
                disciplinas.append(disciplina)

            cursor.close()
            conn.close()

            return disciplinas
        except mysql.connector.Error as err:
            print(f"Erro ao buscar disciplinas: {err}")
            return []

    def get_by_id(self, cod_disciplina):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT cod_disciplina, nome_disciplina, cod_departamento FROM disciplinas WHERE cod_disciplina = %s"
            cursor.execute(query, (cod_disciplina,))

            row = cursor.fetchone()
            if row:
                cod_disciplina, nome_disciplina, cod_departamento = row
                disciplina = Disciplina(cod_disciplina, nome_disciplina, cod_departamento)
            else:
                disciplina = None

            cursor.close()
            conn.close()

            return disciplina
        except mysql.connector.Error as err:
            print(f"Erro ao buscar disciplina por ID: {err}")
            return None

    def save(self, disciplina):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            if disciplina.cod_disciplina:
                # Atualizar disciplina
                query = "UPDATE disciplinas SET nome_disciplina = %s, cod_departamento = %s WHERE cod_disciplina = %s"
                values = (disciplina.nome_disciplina, disciplina.cod_departamento, disciplina.cod_disciplina)
            else:
                # Inserir nova disciplina
                query = "INSERT INTO disciplinas (nome_disciplina, cod_departamento) VALUES (%s, %s)"
                values = (disciplina.nome_disciplina, disciplina.cod_departamento)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar disciplina: {err}")
            return False

    def delete(self, disciplina):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "DELETE FROM disciplinas WHERE cod_disciplina = %s"
            cursor.execute(query, (disciplina.cod_disciplina,))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir disciplina: {err}")
            return False
