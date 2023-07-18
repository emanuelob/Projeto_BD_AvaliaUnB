import os, csv
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

def obter_id_professor(nome_professor, conn):
    cursor = conn.cursor()
    
    # Remove a parte final "(60h)" e espaços extras do nome do professor
    nome_professor = nome_professor.split(" (")[0].rstrip()

    # Consulta para obter o id_professor a partir do nome_professor
    query = "SELECT id_professor FROM professores WHERE nome_professor = %s"
    cursor.execute(query, (nome_professor,))

    # Obtém o resultado da consulta
    result = cursor.fetchone()

    # Fecha o cursor, mas mantém a conexão aberta para uso posterior
    cursor.close()

    # Retorna o id_professor encontrado ou None se não houver correspondência
    return result[0] if result else None

def importar_turmas():
    # Obter o caminho absoluto atual do script Python
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, 'dataCSV', 'turmas_2023_1.csv')

    conn = conectar_bd()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                turma = row['turma']
                periodo = row['periodo']
                cod_disciplina = row['cod_disciplina']
                cod_depto = row['cod_depto']

                # Verifica se o cod_depto é 508 antes de importar a turma
                if cod_depto == '508':
                    # Obtém o id_professor a partir do nome do professor
                    nome_professor = row['professor']
                    id_professor = obter_id_professor(nome_professor, conn)

                    # Insere os dados na tabela turmas
                    query = "INSERT INTO turmas (numero_turma, periodo_turma, id_professor, cod_disciplina) VALUES (%s, %s, %s, %s)"
                    values = (turma, periodo, id_professor, cod_disciplina)
                    cursor.execute(query, values)

        # Salva as alterações no banco de dados
        conn.commit()
        print("Turmas importadas com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao importar os dados: {err}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    importar_turmas()
