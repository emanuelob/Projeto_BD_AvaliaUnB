import mysql.connector

class Denuncia:
    def __init__(self, id_denuncia, id_avaliacao, matricula_estudante, motivo):
        self.id_denuncia = id_denuncia
        self.id_avaliacao = id_avaliacao
        self.matricula_estudante = matricula_estudante
        self.motivo = motivo

class DenunciaDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_denuncia, id_avaliacao, matricula_estudante, motivo FROM denuncias"
            cursor.execute(query)

            denuncias = []
            for row in cursor.fetchall():
                id_denuncia, id_avaliacao, matricula_estudante, motivo = row
                denuncia_obj = Denuncia(id_denuncia, id_avaliacao, matricula_estudante, motivo)
                denuncias.append(denuncia_obj)

            cursor.close()
            conn.close()

            return denuncias
        except mysql.connector.Error as err:
            print(f"Erro ao buscar denuncias: {err}")
            return []

    def get_by_id(self, id_denuncia):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_denuncia, id_avaliacao, matricula_estudante, motivo FROM denuncias WHERE id_denuncia = %s"
            cursor.execute(query, (id_denuncia,))

            row = cursor.fetchone()
            if row:
                id_denuncia, id_avaliacao, matricula_estudante, motivo = row
                denuncia_obj = Denuncia(id_denuncia, id_avaliacao, matricula_estudante, motivo)
            else:
                denuncia_obj = None

            cursor.close()
            conn.close()

            return denuncia_obj
        except mysql.connector.Error as err:
            print(f"Erro ao buscar denuncia por ID: {err}")
            return None

    def save(self, denuncia):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            if denuncia.id_denuncia:
                # Atualizar denuncia
                query = "UPDATE denuncias SET id_avaliacao = %s, matricula_estudante = %s, motivo = %s WHERE id_denuncia = %s"
                values = (denuncia.id_avaliacao, denuncia.matricula_estudante, denuncia.motivo, denuncia.id_denuncia)
            else:
                # Inserir nova denuncia
                query = "INSERT INTO denuncias (id_avaliacao, matricula_estudante, motivo) VALUES (%s, %s, %s)"
                values = (denuncia.id_avaliacao, denuncia.matricula_estudante, denuncia.motivo)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar denuncia: {err}")
            return False

    def delete(self, denuncia):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "DELETE FROM denuncias WHERE id_denuncia = %s"
            cursor.execute(query, (denuncia.id_denuncia,))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir denuncia: {err}")
            return False
