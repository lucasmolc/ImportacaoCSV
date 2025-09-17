#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ferramenta de Importação CSV para SQL Server
# Importa dados de arquivos CSV para bancos de dados SQL Server
# 
# Autor: Lucas Mol
# Versão: 2.1

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
    # Instala pacote se não estiver presente e o importa
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
    # Valida nome da tabela SQL Server de acordo com convenções de nomenclatura
    if not table_name or not table_name.strip():
        return False, "Nome da tabela não pode estar vazio."
    
    table_name = table_name.strip()
    
    # Verifica comprimento (SQL Server max identifier length é 128)
    if len(table_name) > 128:
        return False, "Nome da tabela não pode ter mais de 128 caracteres."
    
    # Verifica caracteres inválidos (alfanuméricos, underscore e # para temp tables)
    # Permite tabelas temporárias que começam com # ou tabelas normais que começam com letra/underscore
    if not re.match(r'^(#[a-zA-Z0-9_]+|[a-zA-Z_][a-zA-Z0-9_]*)$', table_name):
        return False, "Nome da tabela deve começar com letra, underscore ou # (para tabelas temporárias) e conter apenas letras, números e underscores."
    
    # Verifica palavras reservadas do SQL Server
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
    # Valida caminho do arquivo CSV
    if not file_path or not file_path.strip():
        return False, "Caminho do arquivo não pode estar vazio."
    
    file_path = file_path.strip()
    
    # Remove aspas se presentes
    if file_path.startswith('"') and file_path.endswith('"'):
        file_path = file_path[1:-1]
    
    # Verifica se o caminho existe
    if not os.path.exists(file_path):
        return False, "Arquivo não encontrado no caminho especificado."
    
    # Verifica se é um arquivo (não um diretório)
    if not os.path.isfile(file_path):
        return False, "O caminho especificado não é um arquivo."
    
    # Verifica extensão do arquivo
    if not file_path.lower().endswith('.csv'):
        return False, "Arquivo deve ter extensão .csv"
    
    # Verifica se o arquivo é legível
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1)  # Tenta ler o primeiro caractere
    except PermissionError:
        return False, "Sem permissão para ler o arquivo."
    except UnicodeDecodeError:
        # Tenta com diferentes encodings
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                f.read(1)
        except:
            return False, "Não foi possível ler o arquivo. Verifique a codificação."
    except Exception as e:
        return False, f"Erro ao acessar o arquivo: {str(e)}"
    
    return True, file_path

def get_user_input_with_validation(prompt, validator_func, max_attempts=3):
    # Obtém entrada do usuário com validação e mecanismo de retry
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
    # Carrega configuração do arquivo appsettings.json
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
    # Obtém connection string da configuração
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
    # Detecta ambiente baseado no conteúdo da connection string
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
    # Converte connection string do SQL Server para formato SQLAlchemy
    pattern = r"Server=(.*?);Database=(.*?);User Id=(.*?);Password=(.*?);"
    match = re.match(pattern, conn_str, re.IGNORECASE)
    
    if match:
        server = match.group(1)
        database = match.group(2)
        user = match.group(3)
        password = urllib.parse.quote_plus(match.group(4))
        return f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    
    return conn_str

def check_table_exists(db_connection, table_name):
    # Verifica se a tabela existe no banco de dados
    try:
        # Usa SQLAlchemy para verificar se a tabela existe
        inspector = sqlalchemy.inspect(db_connection)
        tables = inspector.get_table_names()
        return table_name.lower() in [t.lower() for t in tables]
    except Exception as e:
        raise Exception(f"Erro ao verificar se a tabela existe: {str(e)}")

def insert_data(db_connection, table_name, data):
    # Insere dados na tabela do banco de dados
    # Verifica se a tabela existe antes de tentar inserir dados
    if not check_table_exists(db_connection, table_name):
        raise Exception(f"❌ Tabela '{table_name}' não existe no banco de dados. "
                       f"Por favor, crie a tabela antes de executar a importação.")
    
    # Insere dados usando modo 'append' (falhará se a tabela não existir devido à nossa verificação acima)
    data.to_sql(table_name, con=db_connection, if_exists='append', index=False)

# ============================================================================
# CSV PROCESSING FUNCTIONS
# ============================================================================

def read_csv(file_path, config=None):
    # Lê arquivo CSV com configurações definidas
    # Obtém configurações de CSV da config ou usa padrões
    separator = ';'
    encoding = 'utf-8'
    
    if config and config.get("Settings"):
        separator = config["Settings"].get("CsvSeparator", ';')
        encoding = config["Settings"].get("CsvEncoding", 'utf-8')
    
    try:
        df = pd.read_csv(file_path, sep=separator, quotechar='"', encoding=encoding)
        # Remove colunas unnamed
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
    # Função principal para processar importação CSV
    # Lê o arquivo CSV
    data = read_csv(csv_file, config)
    
    # Conecta ao banco de dados
    engine = sqlalchemy.create_engine(db_url)
    
    # Valida se a tabela existe antes do processamento
    print(f"🔍 Verificando se a tabela '{table_name}' existe...")
    if not check_table_exists(engine, table_name):
        raise Exception(f"❌ Tabela '{table_name}' não existe no banco de dados. "
                       f"Por favor, crie a tabela antes de executar a importação.")
    
    print(f"✅ Tabela '{table_name}' encontrada no banco de dados")
    
    # Obtém chunk size da config ou usa padrão
    chunk_size = 1000
    if config and config.get("Settings", {}).get("ChunkSize"):
        chunk_size = config["Settings"]["ChunkSize"]
    
    # Insere dados na tabela especificada com barra de progresso
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
    # Exibe cabeçalho da aplicação
    os.system('cls')
    print("=" * 60)
    print("📋 IMPORTAÇÃO DE DADOS CSV PARA SQL SERVER")
    print("=" * 60)

def display_summary(environment, table_name, csv_file, chunk_size):
    # Exibe resumo da importação
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
    # Obtém nome da tabela do usuário com validação
    display_header()
    print("\n📋 Informe o nome da tabela destino:")
    print("   • Deve começar com letra, underscore ou # (tabelas temporárias)")
    print("   • Apenas letras, números e underscores")
    print("   • Máximo 128 caracteres")
    print("   • Não pode ser palavra reservada do SQL")
    print("   ⚠️  A tabela DEVE EXISTIR no banco de dados")
    
    return get_user_input_with_validation(
        "\n➤ Nome da tabela: ",
        validate_table_name
    )

def get_csv_file_path():
    # Obtém caminho do arquivo CSV do usuário com validação
    display_header()
    print("\n📁 Informe o caminho completo do arquivo CSV:")
    print("   • Deve ser um arquivo com extensão .csv")
    print("   • Caminho deve existir e ser acessível")
    print("   • Use aspas se o caminho contiver espaços")
    
    return get_user_input_with_validation(
        "\n➤ Caminho do arquivo CSV: ",
        validate_csv_file_path
    )

def get_user_confirmation():
    # Obtém confirmação do usuário para prosseguir
    confirm = input("\n❓ Deseja prosseguir com a importação? (s/n): ").lower()
    return confirm == 's'

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Ponto de entrada principal da aplicação
    try:
        os.system('cls')
        
        print("🔧 Carregando configurações...")
        
        # Carrega configuração
        config = load_config()
        if not config:
            print("❌ Não foi possível carregar as configurações. Verifique o arquivo appsettings.json")
            return False
        
        # Obtém connection string do banco de dados da config (obrigatório)
        db_url = get_connection_string_from_config(config)
        if not db_url:
            print("❌ Connection string não encontrada na configuração!")
            print("   Verifique se o arquivo appsettings.json está configurado corretamente.")
            return False
        
        # Obtém nome da tabela com validação
        table_name = get_table_name()
        if not table_name:
            print("❌ Nome da tabela inválido. Encerrando aplicação.")
            return False
        
        # Obtém caminho do arquivo CSV com validação
        csv_file = get_csv_file_path()
        if not csv_file:
            print("❌ Caminho do arquivo inválido. Encerrando aplicação.")
            return False
        
        # Mostra resumo antes do processamento
        environment = detect_environment_from_connection_string(db_url)
        chunk_size = config.get('Settings', {}).get('ChunkSize', 1000)
        display_summary(environment, table_name, csv_file, chunk_size)
        
        # Obtém confirmação do usuário
        if not get_user_confirmation():
            print("❌ Importação cancelada pelo usuário.")
            return False
        
        print("\n🚀 Iniciando importação...")
        
        # Processa a importação
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