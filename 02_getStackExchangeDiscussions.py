from utils.linksHandler import read_links_from_file, extract_ids_from_links
from utils.jsonHandler import save_posts_to_json 
from db.getPosts import fetch_posts

input_file = "discussions/all.txt"
output_file = "discussions/discussions.json"


print("Lendo links do arquivo...")
links = read_links_from_file(input_file)

print("Extraindo IDs dos links...")
post_ids = extract_ids_from_links(links)


print("Consultando banco de dados...")
posts = fetch_posts(post_ids)

print(f"Foram recuperadas {len(posts)} discussões")

print("Salvando resultados em JSON...")
save_posts_to_json(posts, output_file)

print("Pipeline concluído!")