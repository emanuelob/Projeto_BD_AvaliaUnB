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

def importar_professores():
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
                professor = row['professor']
                # Remove a parte final "(60h)" e espaços extras do nome do professor
                nome_professor = professor.split(" (")[0].rstrip()

                cod_depto = row['cod_depto']
                # Verifica se o cod_depto é 508 antes de inserir o professor no banco de dados
                if cod_depto == '508':
                    # Verifica se o professor já não está no banco de dados
                    query = "SELECT * FROM professores WHERE nome_professor = %s"
                    values = (nome_professor,)
                    cursor.execute(query, values)

                    if not cursor.fetchone():
                        # Insere o professor no banco de dados
                        query = "INSERT INTO professores (nome_professor, cod_departamento) VALUES (%s, %s)"
                        values = (nome_professor, cod_depto)
                        cursor.execute(query, values)
                        conn.commit()

        print("Professores importados com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao importar os dados: {err}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    importar_professores()
