import re
def read_links_from_file(file_name):
    with open(file_name, "r") as file:
        return [line.strip() for line in file if line.strip()]
    
def extract_ids_from_links(links):
    """
    Extrai IDs de uma lista de URLs.
    """
    ids = []
    for link in links:
        match = re.search(r"/questions/(\d+)", link)
        if match:
            ids.append(int(match.group(1)))
    return ids