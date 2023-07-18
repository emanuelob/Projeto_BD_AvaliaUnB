
import mysql.connector

class Turma:
    def __init__(self, id_turma, numero_turma, periodo_turma, id_professor, cod_disciplina):
        self.id_turma = id_turma
        self.numero_turma = numero_turma
        self.periodo_turma = periodo_turma
        self.id_professor = id_professor
        self.cod_disciplina = cod_disciplina

class TurmaDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_turma, numero_turma, periodo_turma, id_professor, cod_disciplina FROM turmas"
            cursor.execute(query)

            turmas = []
            for row in cursor.fetchall():
                id_turma, numero_turma, periodo_turma, id_professor, cod_disciplina = row
                turma = Turma(id_turma, numero_turma, periodo_turma, id_professor, cod_disciplina)
                turmas.append(turma)

            cursor.close()
            conn.close()

            return turmas
        except mysql.connector.Error as err:
            print(f"Erro ao buscar turmas: {err}")
            return []

    def get_by_id(self, id_turma):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_turma, numero_turma, periodo_turma, id_professor, cod_disciplina FROM turmas WHERE id_turma = %s"
            cursor.execute(query, (id_turma,))

            row = cursor.fetchone()
            if row:
                id_turma, numero_turma, periodo_turma, id_professor, cod_disciplina = row
                turma = Turma(id_turma, numero_turma, periodo_turma, id_professor, cod_disciplina)
            else:
                turma = None

            cursor.close()
            conn.close()

            return turma
        except mysql.connector.Error as err:
            print(f"Erro ao buscar turma por ID: {err}")
            return None

    def save(self, turma):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            if turma.id_turma:
                # Atualizar turma
                query = "UPDATE turmas SET numero_turma = %s, periodo_turma = %s, id_professor = %s, cod_disciplina = %s WHERE id_turma = %s"
                values = (turma.numero_turma, turma.periodo_turma, turma.id_professor, turma.cod_disciplina, turma.id_turma)
            else:
                # Inserir nova turma
                query = "INSERT INTO turmas (numero_turma, periodo_turma, id_professor, cod_disciplina) VALUES (%s, %s, %s, %s)"
                values = (turma.numero_turma, turma.periodo_turma, turma.id_professor, turma.cod_disciplina)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar turma: {err}")
            return False

    def delete(self, turma):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "DELETE FROM turmas WHERE id_turma = %s"
            cursor.execute(query, (turma.id_turma,))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir turma: {err}")
            return False
