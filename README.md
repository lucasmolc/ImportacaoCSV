# CSV to DB Project

This project provides a simple way to read data from a CSV file and insert it into a specified database table.

## Project Structure

```
ImportacaoCSV
├── src
│   ├── main.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Requirements

To run this project, you need to have the following dependencies installed:

- pandas
- sqlalchemy
- pyodbc (if using SQL Server)

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Place your CSV file in a directory accessible to the script.
2. Run the application:

```
python src/main.py
```

3. When prompted, provide:
   - The table name where data will be inserted
   - The database connection string (e.g., for SQL Server: `mssql+pyodbc://usuario:senha@servidor/banco?driver=ODBC+Driver+17+for+SQL+Server`)
   - The file path to your CSV file

## Example

```
Nome da tabela: minha_tabela
ConnectionString: mssql+pyodbc://user:senha@localhost/meubanco?driver=ODBC+Driver+17+for+SQL+Server
FilePath: C:\caminho\para\arquivo.csv
```

This will read the data from the specified CSV file and insert it into the chosen database table.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for this project.