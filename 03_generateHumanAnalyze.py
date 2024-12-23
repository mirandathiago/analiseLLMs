from utils.linksHandler import read_links_from_file, extract_ids_from_links
from utils.jsonHandler import save_posts_to_json, load_json

def process_inclusion(posts_file, included_ids, output_file):
    # Carregar o arquivo JSON com as discussões
    posts = load_json(posts_file)
   
    # Processar cada post e adicionar o campo "Inclusion"
    for post in posts:
        post_id = post.get('id')
        if post_id in included_ids:
            post['Inclusion'] = 'Yes'
        else:
            post['Inclusion'] = 'No'

    # Salvar o arquivo atualizado com a análise humana
    save_posts_to_json(posts,output_file)
    print(f"Arquivo '{output_file}' foi salvo com a análise de inclusão.")


links = read_links_from_file('discussions/included.txt')
ids_incluidos = extract_ids_from_links(links)
id_set = set(map(int, ids_incluidos))
process_inclusion('discussions/discussions.json', id_set, 'analyzed_posts/posts_analisados_humanos.json')
