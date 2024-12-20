from db.connection import connect_database
import xml.etree.ElementTree as ET
import os



def getTableKeys(table):
    """Return an array of the keys for a given table"""
    keys = None
    if table == "Users":
        keys = [
            "Id",
            "Reputation",
            "CreationDate",
            "DisplayName",
            "LastAccessDate",
            "WebsiteUrl",
            "Location",
            "AboutMe",
            "Views",
            "UpVotes",
            "DownVotes",
            "ProfileImageUrl",
            "Age",
            "AccountId",
        ]
    elif table == "Badges":
        keys = ["Id", "UserId", "Name", "Date"]
    elif table == "PostLinks":
        keys = ["Id", "CreationDate", "PostId", "RelatedPostId", "LinkTypeId"]
    elif table == "Comments":
        keys = ["Id", "PostId", "Score", "Text", "CreationDate", "UserId"]
    elif table == "Votes":
        keys = ["Id", "PostId", "VoteTypeId", "UserId", "CreationDate", "BountyAmount"]
    elif table == "Posts":
        keys = [
            "Id",
            "PostTypeId",
            "AcceptedAnswerId",
            "ParentId",
            "CreationDate",
            "Score",
            "ViewCount",
            "Body",
            "OwnerUserId",
            "LastEditorUserId",
            "LastEditorDisplayName",
            "LastEditDate",
            "LastActivityDate",
            "Title",
            "Tags",
            "AnswerCount",
            "CommentCount",
            "FavoriteCount",
            "ClosedDate",
            "CommunityOwnedDate",
        ]
    elif table == "Tags":
        keys = ["Id", "TagName", "Count", "ExcerptPostId", "WikiPostId"]
    elif table == "PostHistory":
        keys = [
            "Id",
            "PostHistoryTypeId",
            "PostId",
            "RevisionGUID",
            "CreationDate",
            "UserId",
            "Text",
        ]
    elif table == "Comments":
        keys = ["Id", "PostId", "Score", "Text", "CreationDate", "UserId"]
    return keys

# Função para processar os arquivos XML e inserir dados nas tabelas
def process_xml_data(xml_file, table_name, conn):
    cursor = conn.cursor()
    table_keys = getTableKeys(table_name)
    
    if not table_keys:
        raise ValueError(f"Tabela '{table_name}' não possui campos definidos.")

    try:
        # Faz a leitura do XML
        for event, elem in ET.iterparse(xml_file, events=('end',)):
            if elem.tag == 'row':  # Cada elemento <row> é um registro
                data = {k: v for k, v in elem.attrib.items() if k in table_keys}
                columns = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(query, list(data.values()))
                elem.clear()  # Libera memória após o processamento do elemento

        conn.commit()  # Confirma as alterações no banco de dados
        print(f"Dados inseridos com sucesso na tabela {table_name} a partir de {xml_file}")

    except Exception as e:
        print(f"Erro ao processar o arquivo {xml_file}: {e}")
        conn.rollback()

# Função principal que coordena a execução
def populate_tables_with_xml(tables_list, xml_folder):
    # Estabelece a conexão com o banco
    conn = connect_database()
    if not conn:
        return

    for table_name in tables_list:
        xml_file = os.path.join(xml_folder, f"{table_name}.xml")  # Caminho do arquivo XML correspondente

        # Verifica se o arquivo XML existe antes de tentar processá-lo
        if os.path.isfile(xml_file):
            print(f"Processando a tabela {table_name} com o arquivo XML {xml_file}.")
            process_xml_data(xml_file, table_name, conn)
        else:
            print(f"Arquivo XML correspondente não encontrado para a tabela {table_name}.")

    conn.close()  # Fecha a conexão com o banco

