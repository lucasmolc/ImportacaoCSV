# CSV Import Tool

Uma aplicação Python profissional para importar dados de arquivos CSV para bancos SQL Server.

## 🚀 Características

- **Validação Rigorosa**: Validação completa de nomes de tabela e arquivos CSV
- **Interface Intuitiva**: Interface visual clara com feedback em tempo real
- **Processamento em Lotes**: Importação otimizada com processamento em chunks
- **Detecção de Ambiente**: Identificação automática do ambiente (Produção/Homologação/Desenvolvimento)
- **Configuração Flexível**: Sistema de configuração baseado em JSON
- **Tratamento de Erros**: Sistema robusto de tratamento de erros e validações
- **Suporte Multi-Encoding**: Suporte automático para UTF-8 e Latin-1

## 📁 Estrutura do Projeto

```
ImportacaoCSV/
├── src/
│   ├── main.py              # Aplicação principal
│   └── utils.py             # Utilitários (futuro)
├── tests/                   # Testes automatizados
│   ├── test_main.py         # Testes unitários
│   ├── run_automated_tests.py # Script de testes
│   └── mock_data/           # Dados para testes
├── appsettings.json         # Configuração da aplicação
├── requirements.txt         # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Esta documentação
```

## ⚙️ Configuração

### appsettings.json

```json
{
  "Database": {
    "ConnectionString": "Server=localhost;Database=ImportacaoCSV;User Id=sa;Password=YourPassword123;"
  },
  "Settings": {
    "ChunkSize": 1000,
    "CsvSeparator": ";",
    "CsvEncoding": "utf-8"
  }
}
```

### Parâmetros de Configuração

- **ConnectionString**: String de conexão com o SQL Server
- **ChunkSize**: Número de registros processados por lote (padrão: 1000)
- **CsvSeparator**: Separador usado no arquivo CSV (padrão: ";")
- **CsvEncoding**: Codificação do arquivo CSV (padrão: "utf-8")

## 🔧 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.7+
- SQL Server com ODBC Driver 17
- Permissões de escrita no banco de dados

### 2. Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd ImportacaoCSV

# As dependências são instaladas automaticamente na primeira execução
# Ou instale manualmente:
pip install -r requirements.txt
```

### 3. Configuração

1. Edite o arquivo `appsettings.json`
2. Configure sua connection string do SQL Server
3. Ajuste as configurações conforme necessário

## 🚀 Como Usar

### Execução Simples

```bash
python src/main.py
```

### Fluxo de Uso

1. **Carregamento**: A aplicação carrega as configurações automaticamente
2. **Nome da Tabela**: Informe o nome da tabela destino (com validação)
3. **Arquivo CSV**: Informe o caminho completo do arquivo CSV
4. **Confirmação**: Revise o resumo e confirme a importação
5. **Processamento**: Acompanhe o progresso da importação

### Exemplo de Execução

```
🔧 Carregando configurações...
✓ Configuração carregada (appsettings.json)
✓ Connection string carregada da configuração

============================================================
📋 IMPORTAÇÃO DE DADOS CSV PARA SQL SERVER
============================================================

📋 Informe o nome da tabela destino:
   • Deve começar com letra ou underscore
   • Apenas letras, números e underscores
   • Máximo 128 caracteres
   • Não pode ser palavra reservada do SQL

➤ Nome da tabela: funcionarios

📁 Informe o caminho completo do arquivo CSV:
   • Deve ser um arquivo com extensão .csv
   • Caminho deve existir e ser acessível
   • Use aspas se o caminho contiver espaços

➤ Caminho do arquivo CSV: C:\dados\funcionarios.csv

============================================================
📊 RESUMO DA IMPORTAÇÃO
============================================================
🎯 Ambiente: Desenvolvimento
🗃️ Tabela destino: funcionarios
📄 Arquivo CSV: C:\dados\funcionarios.csv
📦 Tamanho do lote: 1000
============================================================

❓ Deseja prosseguir com a importação? (s/n): s

🚀 Iniciando importação...
✅ Arquivo CSV lido com sucesso: 1500 registros encontrados
📊 Total de registros a importar: 1500
📦 Tamanho do lote: 1000
Importando linhas: 100%|██████████| 2/2 [00:02<00:00, 1.2it/s]

✅ Importação concluída com sucesso!
```

## 🛡️ Validações Implementadas

### Validação de Nome de Tabela

- ✅ Não pode estar vazio
- ✅ Máximo 128 caracteres
- ✅ Deve começar com letra ou underscore
- ✅ Apenas letras, números e underscores
- ✅ Não pode ser palavra reservada do SQL Server

### Validação de Arquivo CSV

- ✅ Caminho deve existir
- ✅ Deve ser um arquivo (não diretório)
- ✅ Extensão obrigatória: `.csv`
- ✅ Arquivo deve ser legível
- ✅ Suporte para caminhos com aspas
- ✅ Tentativa automática de diferentes encodings

## 🎯 Detecção de Ambiente

A aplicação detecta automaticamente o ambiente baseado na connection string:

- **Produção**: Contém "pjus-producao"
- **Homologação**: Contém "homolog" ou "hml"
- **Desenvolvimento**: Contém "dev" ou "localhost"
- **Personalizado**: Outros casos

## 🧪 Testes

O projeto inclui um sistema completo de testes automatizados:

```bash
# Executar testes automatizados
cd tests
python run_automated_tests.py

# Executar testes com pytest
pytest test_main.py -v
```

## 📊 Características Técnicas

- **Processamento em Chunks**: Otimizado para arquivos grandes
- **Progress Bar**: Feedback visual do progresso
- **Auto-instalação**: Instala dependências automaticamente
- **Tratamento de Encoding**: Suporte UTF-8 e Latin-1
- **Sistema de Retry**: Até 3 tentativas para inputs inválidos
- **Cleanup de Dados**: Remove colunas unnamed automaticamente

## 🔒 Segurança

- Connection strings podem ser configuradas por ambiente
- Validação rigorosa de inputs do usuário
- Proteção contra SQL injection via SQLAlchemy
- Tratamento seguro de senhas com URL encoding

## 🐛 Troubleshooting

### Problemas Comuns

1. **"ODBC Driver not found"**
   - Instale o ODBC Driver 17 for SQL Server

2. **"Permission denied"**
   - Verifique permissões do arquivo CSV
   - Verifique permissões no banco de dados

3. **"Encoding error"**
   - O sistema tenta automaticamente UTF-8 e Latin-1
   - Verifique a codificação do arquivo CSV

4. **"Table not found"**
   - A tabela será criada automaticamente se não existir

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Adicione testes para novas funcionalidades
4. Faça commit das mudanças
5. Push para a branch
6. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

This will read the data from the specified CSV file and insert it into the chosen database table.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for this project.