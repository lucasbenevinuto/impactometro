import pandas as pd
import pymysql

def fetch_data_from_view(host, port, user, password, database, view_name):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        query = f"SELECT * FROM {view_name}"
        df = pd.read_sql(query, connection)
        
        df.columns = [
            "ID", "ID_GRUPO_EIXO","GRUPO_EIXO","ID_EIXO", "EIXO","ID_PLANO", "PLANO","ID_CARGO", "CARGO","ID_CLASSE", "CLASSE","ID_NIVEL", 
            "NIVEL", "SIGLA_EMPRESA", "MATRICULA", "VALOR", 
            "TIPO DE VINCULO"
        ]
        return df
        
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()