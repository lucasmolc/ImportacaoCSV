# Ferramenta de Importação CSV para SQL Server

Uma aplicação Python profissional para importar dados de arquivos CSV para bancos de dados SQL Server com validação rigorosa e controle de integridade.

## 🚀 Características

- **Validação de Tabela**: Verificação obrigatória de existência da tabela antes da importação
- **Validação Rigorosa**: Validação completa de nomes de tabela e arquivos CSV
- **Interface Intuitiva**: Interface visual clara com feedback em tempo real
- **Processamento em Lotes**: Importação otimizada com processamento em chunks
- **Detecção de Ambiente**: Identificação automática do ambiente (Produção/Homologação)
- **Configuração Flexível**: Sistema de configuração baseado em JSON
- **Tratamento de Erros**: Sistema robusto de tratamento de erros e validações
- **Suporte Multi-Encoding**: Suporte automático para UTF-8 e Latin-1
- **Controle de Schema**: Impede criação automática de tabelas no banco de dados

## 📁 Estrutura do Projeto

```
ImportacaoCSV/
├── src/
│   └── main.py              # Aplicação principal
├── appsettings.json         # Configuração da aplicação (ignorado pelo Git)
├── requirements.txt         # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
├── LICENSE                 # Licença do projeto
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

⚠️ **Importante**: O arquivo `appsettings.json` é ignorado pelo Git por questões de segurança. Crie uma cópia local baseada no exemplo acima.

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

1. **Configuração**: Certifique-se de que o arquivo `appsettings.json` está configurado
2. **Preparação**: Verifique se a tabela destino **JÁ EXISTE** no banco de dados
3. **Execução**: Execute a aplicação e siga as instruções
4. **Nome da Tabela**: Informe o nome da tabela destino (com validação)
5. **Arquivo CSV**: Informe o caminho completo do arquivo CSV
6. **Validação**: O sistema verificará se a tabela existe no banco
7. **Confirmação**: Revise o resumo e confirme a importação
8. **Processamento**: Acompanhe o progresso da importação

⚠️ **IMPORTANTE**: A tabela destino DEVE existir no banco de dados. A aplicação NÃO criará tabelas automaticamente.

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
   ⚠️  A tabela DEVE EXISTIR no banco de dados

➤ Nome da tabela: funcionarios

📁 Informe o caminho completo do arquivo CSV:
   • Deve ser um arquivo com extensão .csv
   • Caminho deve existir e ser acessível
   • Use aspas se o caminho contiver espaços

➤ Caminho do arquivo CSV: C:\dados\funcionarios.csv

🔍 Verificando se a tabela 'funcionarios' existe...
✅ Tabela 'funcionarios' encontrada no banco de dados

============================================================
📊 RESUMO DA IMPORTAÇÃO
============================================================
🎯 Ambiente: Homologação
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
- ✅ **Tabela deve existir no banco de dados**

### Validação de Arquivo CSV

- ✅ Caminho deve existir
- ✅ Deve ser um arquivo (não diretório)
- ✅ Extensão obrigatória: `.csv`
- ✅ Arquivo deve ser legível
- ✅ Suporte para caminhos com aspas
- ✅ Tentativa automática de diferentes encodings

### Validação de Banco de Dados

- ✅ Verificação de existência da tabela antes da importação
- ✅ Conexão com o banco validada antes do processamento
- ✅ Tratamento de erros de conectividade

## 🎯 Detecção de Ambiente

A aplicação detecta automaticamente o ambiente baseado na connection string:

- **Produção**: Contém "pjus-producao"
- **Homologação**: Outros casos (padrão)

## 🧪 Testes

O projeto suporta testes manuais através da execução direta:

```bash
# Executar a aplicação para testes
python src/main.py
```

Para testes automatizados, considere implementar validações com dados de mock.

## 📊 Características Técnicas

- **Validação de Tabela**: Verificação obrigatória de existência antes da importação
- **Processamento em Chunks**: Otimizado para arquivos grandes
- **Progress Bar**: Feedback visual do progresso
- **Auto-instalação**: Instala dependências automaticamente
- **Tratamento de Encoding**: Suporte UTF-8 e Latin-1
- **Sistema de Retry**: Até 3 tentativas para inputs inválidos
- **Cleanup de Dados**: Remove colunas unnamed automaticamente
- **Fail-Fast**: Falha rapidamente se requisitos não forem atendidos

## 🔒 Segurança

- Arquivo de configuração ignorado pelo Git (.gitignore)
- Validação rigorosa de inputs do usuário
- Proteção contra SQL injection via SQLAlchemy
- Tratamento seguro de senhas com URL encoding
- Controle de schema - não cria tabelas automaticamente

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

4. **"Tabela não encontrada"**
   - Certifique-se de que a tabela existe no banco de dados
   - A aplicação NÃO cria tabelas automaticamente
   - Verifique se o nome da tabela está correto

5. **"Connection failed"**
   - Verifique a connection string no appsettings.json
   - Confirme se o servidor SQL está acessível
   - Valide as credenciais de acesso

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Adicione testes para novas funcionalidades
4. Faça commit das mudanças
5. Push para a branch
6. Abra um Pull Request