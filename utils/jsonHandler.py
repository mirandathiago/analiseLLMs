import json

def save_posts_to_json(posts, output_file):
    with open(output_file, "w") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
    print(f"JSON salvo em '{output_file}'")