from db.connection import connect_database
import os

def create_tables(sql_files):
    tables = []
    try:
       
        with connect_database() as conn:
            for sql_file in sql_files:
                table_name = os.path.splitext(os.path.basename(sql_file))[0]

                
                with open(sql_file, 'r') as f:
                    script_sql = f.read()
                
                
                with conn.cursor() as cursor:
                    cursor.execute(script_sql)
                    print(f"Tabela {table_name} criada com sucesso.")
                    tables.append(table_name)
            
            conn.commit()
            return tables

    except Exception as e:
        print(f"Erro ao executar ação no banco de dados: {e}")
        conn.rollback()
