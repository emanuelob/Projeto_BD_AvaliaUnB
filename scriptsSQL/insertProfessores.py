import csv
import mysql.connector

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pwd123456',
    'database': 'unbavalia',
}

# Função para inserir dados na tabela de Professores
def insert_professores(data):
    query = "INSERT INTO professores (nome_professor, cod_departamento) VALUES (%s, %s) ON DUPLICATE KEY UPDATE cod_departamento = VALUES(cod_departamento)"

    # Conecta ao banco de dados
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insere os dados na tabela de Professores
    for row in data:
        professor = row['professor']
        cod_depto = row['cod_depto']
        
        # Verifica se o professor já existe no banco de dados
        check_query = "SELECT nome_professor FROM professores WHERE nome_professor = %s"
        cursor.execute(check_query, (professor,))
        result = cursor.fetchone()
        
        if result is None:
            # Se o professor não existe, insere o registro
            values = (professor, cod_depto)
            cursor.execute(query, values)

    # Efetiva as alterações e fecha a conexão
    conn.commit()
    cursor.close()
    conn.close()
    
# Função para ler o arquivo .csv e retornar os dados como uma lista de dicionários
def read_csv_file(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

if __name__ == "__main__":
    # Caminho do arquivo .csv
    csv_file = "dataCSV/turmas_2023_1.csv"

    # Lê os dados do arquivo .csv
    data = read_csv_file(csv_file)

    # Insere os dados na tabela de Professores
    insert_professores(data)