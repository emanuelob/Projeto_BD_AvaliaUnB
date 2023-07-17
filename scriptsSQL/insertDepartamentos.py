import csv
import mysql.connector

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pwd123456',
    'database': 'unbavalia',
}

# Função para inserir dados na tabela de Departamentos
def insert_departamentos(data):
    query = "INSERT INTO departamentos (cod_departamento, nome_departamento) VALUES (%s, %s)"

    # Conecta ao banco de dados
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insere os dados na tabela de Departamentos
    for row in data:
        cod = row['cod']
        nome = row['nome']
        values = (cod, nome)
        cursor.execute(query, values)

    # Efetiva as alterações e fecha a conexão
    conn.commit()
    cursor.close()
    conn.close()

# Função para ler o arquivo CSV e retornar os dados como uma lista de dicionários
def read_csv_file(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

if __name__ == "__main__":
    # Caminho do arquivo CSV
    csv_file = "dataCSV/departamentos_2023_1.csv"

    # Lê os dados do arquivo CSV
    data = read_csv_file(csv_file)

    # Insere os dados na tabela de Departamentos
    insert_departamentos(data)
