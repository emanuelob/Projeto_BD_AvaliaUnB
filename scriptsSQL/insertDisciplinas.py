import csv, os
import mysql.connector

def conectar_bd():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'pwd123456',
        'database': 'unbavalia',
    }

    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def inserir_disciplinas():
    # Obter o caminho absoluto atual do script Python
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, 'dataCSV', 'disciplinas_2023_1.csv')

    conn = conectar_bd()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cod_disciplina = row['cod']
                if cod_disciplina.startswith('CIC'):
                    nome_disciplina = row['nome']
                    cod_departamento = row['cod_depto']

                    # Insere os dados no banco de dados
                    query = "INSERT INTO disciplinas (cod_disciplina, nome_disciplina, cod_departamento) VALUES (%s, %s, %s)"
                    values = (cod_disciplina, nome_disciplina, cod_departamento)
                    cursor.execute(query, values)
                    conn.commit()

        print("Disciplinas inseridas com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao inserir os dados: {err}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    inserir_disciplinas()