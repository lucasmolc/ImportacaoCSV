#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to SQL Server Import Tool
Ferramenta para importação de dados CSV para SQL Server

Author: Lucas Mol
Version: 2.0
"""

import sys
import subprocess
import re
import urllib.parse
import os
import json
from tqdm import tqdm

# ============================================================================
# DEPENDENCY MANAGEMENT
# ============================================================================

def install_and_import(package):
    """Install package if not present and import it"""
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando dependência: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages
for pkg in ["pandas", "sqlalchemy", "pyodbc"]:
    install_and_import(pkg)

import pandas as pd
import sqlalchemy

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_table_name(table_name):
    """Validate SQL Server table name according to naming conventions"""
    if not table_name or not table_name.strip():
        return False, "Nome da tabela não pode estar vazio."
    
    table_name = table_name.strip()
    
    # Check length (SQL Server max identifier length is 128)
    if len(table_name) > 128:
        return False, "Nome da tabela não pode ter mais de 128 caracteres."
    
    # Check for invalid characters (only alphanumeric and underscore allowed)
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
        return False, "Nome da tabela deve começar com letra ou underscore e conter apenas letras, números e underscores."
    
    # Check for SQL Server reserved words
    reserved_words = {
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER', 'TABLE', 'INDEX', 
        'VIEW', 'PROCEDURE', 'FUNCTION', 'TRIGGER', 'DATABASE', 'SCHEMA', 'USER', 'ROLE',
        'ORDER', 'GROUP', 'HAVING', 'WHERE', 'FROM', 'JOIN', 'INNER', 'OUTER', 'LEFT',
        'RIGHT', 'FULL', 'UNION', 'EXCEPT', 'INTERSECT', 'AND', 'OR', 'NOT', 'NULL',
        'TRUE', 'FALSE', 'EXISTS', 'IN', 'LIKE', 'BETWEEN', 'IS', 'AS', 'CASE', 'WHEN',
        'THEN', 'ELSE', 'END', 'BEGIN', 'COMMIT', 'ROLLBACK', 'TRANSACTION'
    }
    
    if table_name.upper() in reserved_words:
        return False, f"'{table_name}' é uma palavra reservada do SQL Server."
    
    return True, "Nome válido."

def validate_csv_file_path(file_path):
    """Validate CSV file path"""
    if not file_path or not file_path.strip():
        return False, "Caminho do arquivo não pode estar vazio."
    
    file_path = file_path.strip()
    
    # Remove quotes if present
    if file_path.startswith('"') and file_path.endswith('"'):
        file_path = file_path[1:-1]
    
    # Check if path exists
    if not os.path.exists(file_path):
        return False, "Arquivo não encontrado no caminho especificado."
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(file_path):
        return False, "O caminho especificado não é um arquivo."
    
    # Check file extension
    if not file_path.lower().endswith('.csv'):
        return False, "Arquivo deve ter extensão .csv"
    
    # Check if file is readable
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1)  # Try to read first character
    except PermissionError:
        return False, "Sem permissão para ler o arquivo."
    except UnicodeDecodeError:
        # Try with different encodings
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                f.read(1)
        except:
            return False, "Não foi possível ler o arquivo. Verifique a codificação."
    except Exception as e:
        return False, f"Erro ao acessar o arquivo: {str(e)}"
    
    return True, file_path

def get_user_input_with_validation(prompt, validator_func, max_attempts=3):
    """Get user input with validation and retry mechanism"""
    for attempt in range(max_attempts):
        user_input = input(prompt).strip()
        is_valid, message = validator_func(user_input)
        
        if is_valid:
            return message if isinstance(message, str) and message != "Nome válido." else user_input
        
        print(f"❌ {message}")
        if attempt < max_attempts - 1:
            print(f"Tentativa {attempt + 1} de {max_attempts}. Tente novamente.\n")
        else:
            print("❌ Número máximo de tentativas excedido.")
            return None
    
    return None

# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

def load_config():
    """Load configuration from appsettings.json"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, 'appsettings.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ Configuração carregada (appsettings.json)")
        return config
    except FileNotFoundError:
        print(f"❌ Arquivo de configuração não encontrado: {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Erro ao ler arquivo de configuração: {config_path}")
        return None

def get_connection_string_from_config(config):
    """Get connection string from config"""
    if not config:
        return None
        
    database_config = config.get("Database", {})
    conn_str = database_config.get("ConnectionString", "")
    
    if conn_str:
        print("✓ Connection string carregada da configuração")
        return conn_str
    
    print("❌ Connection string não encontrada na configuração")
    return None

def detect_environment_from_connection_string(conn_str):
    """Detect environment based on connection string content"""
    if not conn_str:
        return "Desconhecido"
    
    conn_str_lower = conn_str.lower()
    
    if "pjus-producao" in conn_str_lower:
        return "Produção"
    else:
        return "Homologação"

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def convert_sqlserver_conn_str(conn_str):
    """Convert SQL Server connection string to SQLAlchemy format"""
    pattern = r"Server=(.*?);Database=(.*?);User Id=(.*?);Password=(.*?);"
    match = re.match(pattern, conn_str, re.IGNORECASE)
    
    if match:
        server = match.group(1)
        database = match.group(2)
        user = match.group(3)
        password = urllib.parse.quote_plus(match.group(4))
        return f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    
    return conn_str

def insert_data(db_connection, table_name, data):
    """Insert data into database table"""
    data.to_sql(table_name, con=db_connection, if_exists='append', index=False)

# ============================================================================
# CSV PROCESSING FUNCTIONS
# ============================================================================

def read_csv(file_path, config=None):
    """Read CSV file with configuration settings"""
    # Get CSV settings from config or use defaults
    separator = ';'
    encoding = 'utf-8'
    
    if config and config.get("Settings"):
        separator = config["Settings"].get("CsvSeparator", ';')
        encoding = config["Settings"].get("CsvEncoding", 'utf-8')
    
    try:
        df = pd.read_csv(file_path, sep=separator, quotechar='"', encoding=encoding)
        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        print(f"✅ Arquivo CSV lido com sucesso: {len(df)} registros encontrados")
        return df
    except UnicodeDecodeError:
        print(f"⚠ Erro de codificação com {encoding}, tentando latin-1...")
        try:
            df = pd.read_csv(file_path, sep=separator, quotechar='"', encoding='latin-1')
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            print(f"✅ Arquivo CSV lido com sucesso: {len(df)} registros encontrados")
            return df
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo CSV: {str(e)}")
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo CSV: {str(e)}")

# ============================================================================
# MAIN PROCESSING FUNCTION
# ============================================================================

def process_import(csv_file, db_url, table_name, config=None):
    """Main function to process CSV import"""
    # Read the CSV file
    data = read_csv(csv_file, config)
    
    # Connect to the database
    engine = sqlalchemy.create_engine(db_url)
    
    # Get chunk size from config or use default
    chunk_size = 1000
    if config and config.get("Settings", {}).get("ChunkSize"):
        chunk_size = config["Settings"]["ChunkSize"]
    
    # Insert data into the specified table with progress bar
    total = len(data)
    print(f"📊 Total de registros a importar: {total}")
    print(f"📦 Tamanho do lote: {chunk_size}")
    
    for start in tqdm(range(0, total, chunk_size), desc="Importando linhas"):
        end = min(start + chunk_size, total)
        chunk = data.iloc[start:end]
        insert_data(engine, table_name, chunk)

# ============================================================================
# USER INTERFACE FUNCTIONS
# ============================================================================

def display_header():
    """Display application header"""
    print("=" * 60)
    print("📋 IMPORTAÇÃO DE DADOS CSV PARA SQL SERVER")
    print("=" * 60)

def display_summary(environment, table_name, csv_file, chunk_size):
    """Display import summary"""
    os.system('cls')
    print("=" * 60)
    print("� RESUMO DA IMPORTAÇÃO")
    print("=" * 60)
    print(f"🎯 Ambiente: {environment}")
    print(f"🗃️  Tabela destino: {table_name}")
    print(f"📄 Arquivo CSV: {csv_file}")
    print(f"📦 Tamanho do lote: {chunk_size}")
    print("=" * 60)

def get_table_name():
    """Get table name from user with validation"""
    print("\n📋 Informe o nome da tabela destino:")
    print("   • Deve começar com letra ou underscore")
    print("   • Apenas letras, números e underscores")
    print("   • Máximo 128 caracteres")
    print("   • Não pode ser palavra reservada do SQL")
    
    return get_user_input_with_validation(
        "\n➤ Nome da tabela: ",
        validate_table_name
    )

def get_csv_file_path():
    """Get CSV file path from user with validation"""
    print("\n📁 Informe o caminho completo do arquivo CSV:")
    print("   • Deve ser um arquivo com extensão .csv")
    print("   • Caminho deve existir e ser acessível")
    print("   • Use aspas se o caminho contiver espaços")
    
    return get_user_input_with_validation(
        "\n➤ Caminho do arquivo CSV: ",
        validate_csv_file_path
    )

def get_user_confirmation():
    """Get user confirmation to proceed"""
    confirm = input("\n❓ Deseja prosseguir com a importação? (s/n): ").lower()
    return confirm == 's'

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    try:
        os.system('cls')
        
        print("🔧 Carregando configurações...")
        
        # Load configuration
        config = load_config()
        if not config:
            print("❌ Não foi possível carregar as configurações. Verifique o arquivo appsettings.json")
            input("Pressione Enter para sair...")
            return False
        
        # Get database connection string from config (required)
        db_url = get_connection_string_from_config(config)
        if not db_url:
            print("❌ Connection string não encontrada na configuração!")
            print("   Verifique se o arquivo appsettings.json está configurado corretamente.")
            input("Pressione Enter para sair...")
            return False
        
        display_header()
        
        # Get table name with validation
        table_name = get_table_name()
        if not table_name:
            print("❌ Nome da tabela inválido. Encerrando aplicação.")
            input("Pressione Enter para sair...")
            return False
        
        # Get CSV file path with validation
        csv_file = get_csv_file_path()
        if not csv_file:
            print("❌ Caminho do arquivo inválido. Encerrando aplicação.")
            input("Pressione Enter para sair...")
            return False
        
        # Show summary before processing
        environment = detect_environment_from_connection_string(db_url)
        chunk_size = config.get('Settings', {}).get('ChunkSize', 1000)
        display_summary(environment, table_name, csv_file, chunk_size)
        
        # Get user confirmation
        if not get_user_confirmation():
            print("❌ Importação cancelada pelo usuário.")
            input("Pressione Enter para sair...")
            return False
        
        print("\n🚀 Iniciando importação...")
        
        # Process the import
        db_url = convert_sqlserver_conn_str(db_url)
        process_import(csv_file, db_url, table_name, config)
        
        print("\n✅ Importação concluída com sucesso!")
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Importação interrompida pelo usuário.")
        return False
    except Exception as e:
        print(f"\n❌ Erro durante a importação: {str(e)}")
        return False
    finally:
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)