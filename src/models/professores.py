import mysql.connector

class Professor:
    def __init__(self, id_professor, nome_professor, email_professor, cod_departamento):
        self.id_professor = id_professor
        self.nome_professor = nome_professor
        self.email_professor = email_professor
        self.cod_departamento = cod_departamento

class ProfessorDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_professor, nome_professor, email_professor, cod_departamento FROM professores"
            cursor.execute(query)

            professores = []
            for row in cursor.fetchall():
                id_professor, nome_professor, email_professor, cod_departamento = row
                professor = Professor(id_professor, nome_professor, email_professor, cod_departamento)
                professores.append(professor)

            cursor.close()
            conn.close()

            return professores
        except mysql.connector.Error as err:
            print(f"Erro ao buscar professores: {err}")
            return []

    def get_by_id(self, id_professor):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_professor, nome_professor, email_professor, cod_departamento FROM professores WHERE id_professor = %s"
            cursor.execute(query, (id_professor,))

            row = cursor.fetchone()
            if row:
                id_professor, nome_professor, email_professor, cod_departamento = row
                professor = Professor(id_professor, nome_professor, email_professor, cod_departamento)
            else:
                professor = None

            cursor.close()
            conn.close()

            return professor
        except mysql.connector.Error as err:
            print(f"Erro ao buscar professor por ID: {err}")
            return None

    def save(self, professor):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            if professor.id_professor:
                # Atualizar professor
                query = "UPDATE professores SET nome_professor = %s, email_professor = %s, cod_departamento = %s WHERE id_professor = %s"
                values = (professor.nome_professor, professor.email_professor, professor.cod_departamento, professor.id_professor)
            else:
                # Inserir novo professor
                query = "INSERT INTO professores (nome_professor, email_professor, cod_departamento) VALUES (%s, %s, %s)"
                values = (professor.nome_professor, professor.email_professor, professor.cod_departamento)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar professor: {err}")
            return False

    def delete(self, professor):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "DELETE FROM professores WHERE id_professor = %s"
            cursor.execute(query, (professor.id_professor,))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir professor: {err}")
            return False
