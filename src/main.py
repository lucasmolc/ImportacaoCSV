import sys
import subprocess
import re
import urllib.parse
import os

# Instala dependências se não estiverem presentes
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando dependência: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["pandas", "sqlalchemy", "pyodbc"]:
    install_and_import(pkg)

import pandas as pd
import sqlalchemy
from tqdm import tqdm

def convert_sqlserver_conn_str(conn_str):
    # Detecta se está no padrão SQL Server nativo
    pattern = r"Server=(.*?);Database=(.*?);User Id=(.*?);Password=(.*?);"
    match = re.match(pattern, conn_str, re.IGNORECASE)
    if match:
        server = match.group(1)
        database = match.group(2)
        user = match.group(3)
        password = urllib.parse.quote_plus(match.group(4))
        # Monta a connection string para SQLAlchemy com pyodbc
        return f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    return conn_str

def main(csv_file, db_url, table_name):
    # Read the CSV file
    data = read_csv(csv_file)
    
    # Connect to the database
    engine = sqlalchemy.create_engine(db_url)
    
    # Insert data into the specified table with progress bar
    chunk_size = 1000
    total = len(data)
    for start in tqdm(range(0, total, chunk_size), desc="Importando linhas"):
        end = min(start + chunk_size, total)
        chunk = data.iloc[start:end]
        insert_data(engine, table_name, chunk)

def read_csv(file_path):
    df = pd.read_csv(file_path, sep=';', quotechar='"', encoding='utf-8')
    # Remove colunas extras não nomeadas
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def insert_data(db_connection, table_name, data):
    data.to_sql(table_name, con=db_connection, if_exists='append', index=False)

if __name__ == "__main__":
    os.system('cls')
    db_url = input("Informe a ConnectionString do banco: ")
    os.system('cls')
    table_name = input("Informe o nome da tabela destino: ")
    os.system('cls')
    csv_file = input("Informe o caminho do arquivo CSV: ")
    os.system('cls')
    print("Iniciando importação com os parâmetros:")
    print(f"Banco de dados: {db_url}")
    print(f"Tabela destino: {table_name}")
    print(f"Arquivo CSV: {csv_file}")
    db_url = convert_sqlserver_conn_str(db_url)
    main(csv_file, db_url, table_name)