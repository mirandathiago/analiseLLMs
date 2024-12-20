import os
def list_sql_files_with_xml(folder_sql, folder_xml):
   
    sql_files = []
    
   
    for sql_file in os.listdir(folder_sql):
        if sql_file.lower().endswith(".sql"):
           
            xml_file = os.path.splitext(sql_file)[0] + ".xml"
            
           
            xml_file_path = os.path.join(folder_xml, xml_file)
            
            # Verifica se o arquivo XML existe na pasta dump
            if os.path.isfile(xml_file_path):
                # Se o arquivo XML existir, inclui o arquivo SQL na lista
                sql_files.append(os.path.join(folder_sql, sql_file))
                print(f"Arquivo XML correspondente encontrado: {xml_file_path}")

    sql_files.sort()
    return sql_files