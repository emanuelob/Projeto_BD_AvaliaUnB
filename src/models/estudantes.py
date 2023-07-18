import mysql.connector

class Estudante:
    def __init__(self, id_estudante, matricula_estudante, nome_estudante, curso_estudante,
                 email_estudante, senha_estudante, cargo_estudante, foto_estudante):
        self.id_estudante = id_estudante
        self.matricula_estudante = matricula_estudante
        self.nome_estudante = nome_estudante
        self.curso_estudante = curso_estudante
        self.email_estudante = email_estudante
        self.senha_estudante = senha_estudante
        self.cargo_estudante = cargo_estudante
        self.foto_estudante = foto_estudante

class EstudanteDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def validar_credenciais(self, email, senha):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_estudante FROM estudantes WHERE email_estudante = %s AND senha_estudante = %s"
            values = (email, senha)
            cursor.execute(query, values)

            row = cursor.fetchone()
            if row:
                # Se encontrou um estudante com o email e senha fornecidos, as credenciais são válidas
                estudante_id = row[0]
                return estudante_id
            else:
                # Se não encontrou um estudante correspondente, as credenciais são inválidas
                return None
        except mysql.connector.Error as err:
            print(f"Erro ao validar credenciais: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_estudante, matricula_estudante, nome_estudante, curso_estudante, email_estudante, " \
                    "senha_estudante, cargo_estudante, foto_estudante FROM estudantes"
            cursor.execute(query)

            estudantes = []
            for row in cursor.fetchall():
                id_estudante, matricula_estudante, nome_estudante, curso_estudante, email_estudante, \
                senha_estudante, cargo_estudante, foto_estudante = row
                estudante = Estudante(id_estudante, matricula_estudante, nome_estudante, curso_estudante,
                                      email_estudante, senha_estudante, cargo_estudante, foto_estudante)
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

            query = "SELECT id_estudante, matricula_estudante, nome_estudante, curso_estudante, email_estudante, " \
                    "senha_estudante, cargo_estudante, foto_estudante " \
                    "FROM estudantes WHERE id_estudante = %s"
            cursor.execute(query, (id_estudante,))

            row = cursor.fetchone()
            if row:
                id_estudante, matricula_estudante, nome_estudante, curso_estudante, email_estudante, \
                senha_estudante, cargo_estudante, foto_estudante = row
                estudante = Estudante(id_estudante, matricula_estudante, nome_estudante, curso_estudante,
                                      email_estudante, senha_estudante, cargo_estudante, foto_estudante)
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
                query = "UPDATE estudantes SET matricula_estudante = %s, nome_estudante = %s, curso_estudante = %s, email_estudante = %s, senha_estudante = %s, cargo_estudante = %s, foto_estudante = %s WHERE id_estudante = %s"
                values = (estudante.matricula_estudante, estudante.nome_estudante, estudante.curso_estudante, estudante.email_estudante, estudante.senha_estudante, estudante.cargo_estudante, estudante.foto_estudante, estudante.id_estudante)
            else:
                # Inserir novo estudante
                query = "INSERT INTO estudantes (matricula_estudante, nome_estudante, curso_estudante, email_estudante, senha_estudante, cargo_estudante, foto_estudante) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (estudante.matricula_estudante, estudante.nome_estudante, estudante.curso_estudante, estudante.email_estudante, estudante.senha_estudante, estudante.cargo_estudante, estudante.foto_estudante)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar estudante: {err}")
            return False
        except Exception as ex:
            print(f"Erro inesperado ao salvar estudante: {ex}")
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
        except Exception as ex:
            print(f"Erro inesperado ao excluir estudante: {ex}")
            return False