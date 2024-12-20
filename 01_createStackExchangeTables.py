import os
from db.createTables import create_tables
from utils.ListFilesHandler import list_sql_files_with_xml
from db.populateTables import populate_tables_with_xml

 # Define os diretórios onde os arquivos SQL e XML estão localizados

folder_sql = os.path.join('db','schemas')
folder_xml = 'dump'
    
# Lista os arquivos SQL que possuem um correspondente XML
sql_files = list_sql_files_with_xml(folder_sql, folder_xml)

# Criar as tabelas com os arquivos SQL encontrados
tables = create_tables(sql_files)

populate_tables_with_xml(tables,folder_xml)