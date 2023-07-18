import mysql.connector

class Avaliacao:
    def __init__(self, id_avaliacao, matricula_estudante, id_turma, avaliacao, nota):
        self.id_avaliacao = id_avaliacao
        self.matricula_estudante = matricula_estudante
        self.id_turma = id_turma
        self.avaliacao = avaliacao
        self.nota = nota

class AvaliacaoDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_avaliacao, matricula_estudante, id_turma, avaliacao, nota FROM avaliacoes"
            cursor.execute(query)

            avaliacoes = []
            for row in cursor.fetchall():
                id_avaliacao, matricula_estudante, id_turma, avaliacao, nota = row
                avaliacao_obj = Avaliacao(id_avaliacao, matricula_estudante, id_turma, avaliacao, nota)
                avaliacoes.append(avaliacao_obj)

            cursor.close()
            conn.close()

            return avaliacoes
        except mysql.connector.Error as err:
            print(f"Erro ao buscar avaliacoes: {err}")
            return []

    def get_by_id(self, id_avaliacao):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT id_avaliacao, matricula_estudante, id_turma, avaliacao, nota FROM avaliacoes WHERE id_avaliacao = %s"
            cursor.execute(query, (id_avaliacao,))

            row = cursor.fetchone()
            if row:
                id_avaliacao, matricula_estudante, id_turma, avaliacao, nota = row
                avaliacao_obj = Avaliacao(id_avaliacao, matricula_estudante, id_turma, avaliacao, nota)
            else:
                avaliacao_obj = None

            cursor.close()
            conn.close()

            return avaliacao_obj
        except mysql.connector.Error as err:
            print(f"Erro ao buscar avaliacao por ID: {err}")
            return None

    def save(self, avaliacao):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            if avaliacao.id_avaliacao:
                # Atualizar avaliacao
                query = "UPDATE avaliacoes SET matricula_estudante = %s, id_turma = %s, avaliacao = %s, nota = %s WHERE id_avaliacao = %s"
                values = (avaliacao.matricula_estudante, avaliacao.id_turma, avaliacao.avaliacao, avaliacao.nota, avaliacao.id_avaliacao)
            else:
                # Inserir nova avaliacao
                query = "INSERT INTO avaliacoes (matricula_estudante, id_turma, avaliacao, nota) VALUES (%s, %s, %s, %s)"
                values = (avaliacao.matricula_estudante, avaliacao.id_turma, avaliacao.avaliacao, avaliacao.nota)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar avaliacao: {err}")
            return False

    def delete(self, avaliacao):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "DELETE FROM avaliacoes WHERE id_avaliacao = %s"
            cursor.execute(query, (avaliacao.id_avaliacao,))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir avaliacao: {err}")
            return False
