import mysql.connector

#Falta atualizar/adicionar os outros atributos
class Estudante:
    def __init__(self, id_estudante, matricula, nome, email, curso):
        self.id_estudante = id_estudante
        self.matricula = matricula
        self.nome = nome
        self.email = email
        self.curso = curso

class EstudanteDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_estudante, matricula, nome, email, curso FROM estudantes"
            cursor.execute(query)

            estudantes = []
            for row in cursor.fetchall():
                id_estudante, matricula, nome, email, curso = row
                estudante = Estudante(id_estudante, matricula, nome, email, curso)
                estudantes.append(estudante)

            cursor.close()
            conn.close()

            return estudantes
        except mysql.connector.Error as err:
            print(f"Erro ao buscar estudantes: {err}")
            return []

    def get_by_id(self, id_estudante):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_estudante, matricula, nome, email, curso FROM estudantes WHERE id_estudante = %s"
            cursor.execute(query, (id_estudante,))

            row = cursor.fetchone()
            if row:
                id_estudante, matricula, nome, email, curso = row
                estudante = Estudante(id_estudante, matricula, nome, email, curso)
            else:
                estudante = None

            cursor.close()
            conn.close()

            return estudante
        except mysql.connector.Error as err:
            print(f"Erro ao buscar estudante por ID: {err}")
            return None

    def save(self, estudante):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            if estudante.id_estudante:
                # Atualizar estudante
                query = "UPDATE estudantes SET matricula = %s, nome = %s, email = %s, curso = %s WHERE id_estudante = %s"
                values = (estudante.matricula, estudante.nome, estudante.email, estudante.curso, estudante.id_estudante)
            else:
                # Inserir novo estudante
                query = "INSERT INTO estudantes (matricula, nome, email, curso) VALUES (%s, %s, %s, %s)"
                values = (estudante.matricula, estudante.nome, estudante.email, estudante.curso)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar estudante: {err}")
            return False

    def delete(self, estudante):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "DELETE FROM estudantes WHERE id_estudante = %s"
            cursor.execute(query, (estudante.id_estudante,))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir estudante: {err}")
            return False
