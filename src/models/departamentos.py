import mysql.connector

class Departamento:
    def __init__(self, cod_departamento, nome_departamento):
        self.cod_departamento = cod_departamento
        self.nome_departamento = nome_departamento

class DepartamentoDAO:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT cod_departamento, nome_departamento FROM departamentos"
            cursor.execute(query)

            departamentos = []
            for row in cursor.fetchall():
                cod_departamento, nome_departamento = row
                departamento = Departamento(cod_departamento, nome_departamento)
                departamentos.append(departamento)

            cursor.close()
            conn.close()

            return departamentos
        except mysql.connector.Error as err:
            print(f"Erro ao buscar departamentos: {err}")
            return []

    def get_by_id(self, cod_departamento):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "SELECT cod_departamento, nome_departamento FROM departamentos WHERE cod_departamento = %s"
            cursor.execute(query, (cod_departamento,))

            row = cursor.fetchone()
            if row:
                cod_departamento, nome_departamento = row
                departamento = Departamento(cod_departamento, nome_departamento)
            else:
                departamento = None

            cursor.close()
            conn.close()

            return departamento
        except mysql.connector.Error as err:
            print(f"Erro ao buscar departamento por ID: {err}")
            return None

    def save(self, departamento):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            if departamento.cod_departamento:
                # Atualizar departamento
                query = "UPDATE departamentos SET nome_departamento = %s WHERE cod_departamento = %s"
                values = (departamento.nome_departamento, departamento.cod_departamento)
            else:
                # Inserir novo departamento
                query = "INSERT INTO departamentos (nome_departamento) VALUES (%s)"
                values = (departamento.nome_departamento,)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao salvar departamento: {err}")
            return False

    def delete(self, departamento):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            query = "DELETE FROM departamentos WHERE cod_departamento = %s"
            cursor.execute(query, (departamento.cod_departamento,))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir departamento: {err}")
            return False
