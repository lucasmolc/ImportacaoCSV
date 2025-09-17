# Ferramenta de Importação CSV para SQL Server

Uma aplicação Python profissional para importar dados de arquivos CSV para bancos de dados SQL Server com validação rigorosa, controle de integridade e **verificação automática de estruturas de tabela**.

## 🚀 Características

- **Validação de Tabela**: Verificação obrigatória de existência da tabela antes da importação
- **Verificação de Estrutura**: Análise automática da estrutura da tabela "ImportacaoCSV" existente
- **Suporte a Tabelas Temporárias**: Compatibilidade com tabelas temporárias do SQL Server (#tabelas)
- **Validação Rigorosa**: Validação completa de nomes de tabela e arquivos CSV
- **Interface Intuitiva**: Interface visual clara com feedback em tempo real e exibição de estrutura
- **Processamento em Lotes**: Importação otimizada com processamento em chunks
- **Detecção de Ambiente**: Identificação automática do ambiente (Produção/Homologação)
- **Configuração Flexível**: Sistema de configuração baseado em JSON
- **Tratamento de Erros**: Sistema robusto de tratamento de erros e validações
- **Suporte Multi-Encoding**: Suporte automático para UTF-8 e Latin-1
- **Análise de Schema**: Exibição detalhada de colunas, tipos e propriedades das tabelas

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

#### Para Tabelas Existentes:
1. **Configuração**: Certifique-se de que o arquivo `appsettings.json` está configurado
2. **Preparação**: Verifique se a tabela destino **JÁ EXISTE** no banco de dados
3. **Execução**: Execute a aplicação e siga as instruções
4. **Nome da Tabela**: Informe o nome completo da tabela existente
5. **Arquivo CSV**: Informe o caminho completo do arquivo CSV
6. **Validação**: O sistema verificará se a tabela existe no banco
7. **Confirmação**: Revise o resumo e confirme a importação
8. **Processamento**: Acompanhe o progresso da importação

#### Para Verificar Tabela "ImportacaoCSV" Existente:
1. **Preparação**: Certifique-se de que a tabela "ImportacaoCSV" já existe no banco
2. **Configuração**: Certifique-se de que o arquivo `appsettings.json` está configurado
3. **Execução**: Execute a aplicação e siga as instruções
4. **Nome da Tabela**: Digite apenas `#` (sustenido)
5. **Verificação**: A aplicação verifica se a tabela "ImportacaoCSV" existe
6. **Estrutura**: Exibe a estrutura completa da tabela (colunas, tipos, propriedades)
7. **Confirmação**: Confirme se a estrutura está adequada para sua importação
8. **Arquivo CSV**: Informe o caminho completo do arquivo CSV
9. **Processamento**: Acompanhe o progresso da importação

💡 **FUNCIONALIDADE**: Digite `#` para verificar automaticamente a estrutura da tabela "ImportacaoCSV" existente!

### Exemplo de Execução

```
🔧 Carregando configurações...
✓ Configuração carregada (appsettings.json)
✓ Connection string carregada da configuração

============================================================
📋 IMPORTAÇÃO DE DADOS CSV PARA SQL SERVER
============================================================

📋 Informe o nome da tabela destino:
   • Para tabela existente: digite o nome completo
   • Para VERIFICAR tabela 'ImportacaoCSV': digite apenas '#'
   • Nomes devem começar com letra, underscore ou #
   • Apenas letras, números e underscores
   • Máximo 128 caracteres
   • Não pode ser palavra reservada do SQL
   💡 Se digitar '#', será verificada a existência e estrutura da tabela 'ImportacaoCSV'

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

## 🔧 Criando a Tabela "ImportacaoCSV" Manualmente

Para usar a funcionalidade especial `#`, você deve criar a tabela "ImportacaoCSV" previamente no banco de dados. Exemplo de comando SQL:

```sql
-- Exemplo básico de tabela ImportacaoCSV
CREATE TABLE ImportacaoCSV (
    Nome NVARCHAR(100) NOT NULL,
    Email NVARCHAR(150) NULL,
    Idade INT NULL,
    DataNascimento DATETIME NULL,
    Salario DECIMAL(10,2) NULL,
    Ativo BIT NOT NULL DEFAULT 1
);
```

### Dicas para Criação da Tabela:

- **Nomes de colunas**: Use nomes descritivos e sem espaços
- **Tipos de dados**: Escolha tipos adequados para seus dados CSV
- **Tamanhos**: Para NVARCHAR/VARCHAR, use tamanhos suficientes
- **NULL/NOT NULL**: Configure conforme suas regras de negócio
- **Valores padrão**: Considere usar DEFAULT para colunas obrigatórias

### Exemplo de Verificação de Tabela "ImportacaoCSV"

```
➤ Nome da tabela: #

============================================================
� VERIFICAÇÃO DA TABELA ImportacaoCSV
============================================================

✅ Tabela 'ImportacaoCSV' encontrada!

� Estrutura atual da tabela:
--------------------------------------------------
   1. Nome                 NVARCHAR(100)       NOT NULL
   2. Idade                INT                 NULL
   3. DataNascimento       DATETIME            NULL
   4. Salario              DECIMAL(10,2)       NULL
   5. Ativo                BIT                 NOT NULL
--------------------------------------------------
Total de colunas: 5

❓ A estrutura da tabela 'ImportacaoCSV' está adequada para sua importação?
   s = Sim, continuar com a importação
   n = Não, encerrar aplicação

➤ Confirma a estrutura? (s/n): s

✅ Estrutura confirmada! Prosseguindo com a importação...
```

### Exemplo se Tabela Não Existir

```
➤ Nome da tabela: #

============================================================
� VERIFICAÇÃO DA TABELA ImportacaoCSV
============================================================

❌ A tabela 'ImportacaoCSV' não existe no banco de dados.
   Para usar esta funcionalidade, a tabela deve existir previamente.
   Crie a tabela manualmente ou use outro nome de tabela.

❌ Verificação da tabela ImportacaoCSV falhou. Encerrando aplicação.
```

## 🛡️ Validações Implementadas

### Validação de Nome de Tabela

- ✅ Não pode estar vazio
- ✅ Máximo 128 caracteres
- ✅ Deve começar com letra, underscore ou # (tabelas temporárias)
- ✅ Apenas letras, números e underscores
- ✅ Não pode ser palavra reservada do SQL Server
- ✅ **Tabela deve existir no banco de dados** (exceto ao usar `#`)
- ✅ **Suporte especial**: Digite `#` para verificar tabela "ImportacaoCSV"

### Validação de Verificação de Tabela

- ✅ Existência da tabela: verifica se "ImportacaoCSV" existe no banco
- ✅ Estrutura completa: exibe todas as colunas com detalhes
- ✅ Tipos de dados: mostra tipos formatados (NVARCHAR(100), INT, etc.)
- ✅ Propriedades NULL: indica se cada coluna aceita valores nulos
- ✅ Confirmação do usuário: permite validar se estrutura está adequada
- ✅ Fail-safe: encerra aplicação se tabela não existir ou não for confirmada

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
   - Para tabelas existentes: certifique-se de que existe no banco
   - Para criar nova tabela: use `#` como nome da tabela
   - Verifique se o nome da tabela está correto

5. **"Connection failed"**
   - Verifique a connection string no appsettings.json
   - Confirme se o servidor SQL está acessível
   - Valide as credenciais de acesso

6. **"Tabela ImportacaoCSV não existe"**
   - A funcionalidade `#` requer que a tabela "ImportacaoCSV" já exista
   - Crie a tabela manualmente no banco de dados antes de usar
   - Use outro nome de tabela se não quiser criar a "ImportacaoCSV"

7. **"Estrutura da tabela não adequada"**
   - Revise a estrutura exibida pela aplicação
   - Ajuste as colunas da tabela conforme necessário
   - Certifique-se de que os tipos de dados são compatíveis com seu CSV

8. **"Tabelas temporárias não funcionam"**
   - Tabelas temporárias (#) são específicas da sessão
   - Para tabelas temporárias reais, use nomes que começam com #
   - A funcionalidade `#` especial é apenas para a tabela "ImportacaoCSV"

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Adicione testes para novas funcionalidades
4. Faça commit das mudanças
5. Push para a branch
6. Abra um Pull Request