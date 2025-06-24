def read_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def insert_data(db_connection, table_name, data):
    data.to_sql(table_name, con=db_connection, if_exists='append', index=False)