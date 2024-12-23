import json
import time
from tqdm import tqdm
from llms.gemini_1_5 import analyze_with_gemini_1_5
from llms.gemini_2_0 import analyze_with_gemini_2_0
from llms.claude_3_2 import analyze_with_claude
from llms.gpt_4o_mini import analyze_with_chatgpt4omini
from llms.gpt_4o import analyze_with_chatgpt4o
from utils.jsonHandler import load_json

# Função genérica para processar discussões
def process_discussions(discussions, system_prompt, analyze_function, output_file):
    requests = 0
    analyzed_discussions = []
    
    with tqdm(total=len(discussions), desc=f"Discussions", unit="Discussion", leave=False) as disc_pbar:
        for discussion in discussions:
            analysis = analyze_function(discussion["title"], discussion["body"],system_prompt)
            discussion.update(analysis)
            analyzed_discussions.append(discussion)
            requests += 1
            disc_pbar.update(1)
            if requests % 5 == 0:
                time.sleep(60)  # Evitar limitação de taxa

    # Salvar resultados
    with open(output_file, "w") as f:
        json.dump(analyzed_discussions, f, indent=4)
    print(f"Análise concluída. Resultados salvos em '{output_file}'.")

def load_system_prompt(filepath):
     # Carregar prompt do sistema
    with open(filepath, "r") as f:
        system_prompt = f.read().strip()
    return system_prompt


# Pipeline principal
if __name__ == "__main__":

    discussions = load_json("discussions/discussions.json")
    
    system_prompt = load_system_prompt("prompts/system_prompt_fewshot.txt")


    process_discussions(discussions, system_prompt, analyze_with_gemini_1_5, "analyzed_posts/posts_gemini_1_5.json")
   
    process_discussions(discussions, system_prompt, analyze_with_gemini_2_0, "analyzed_posts/posts_gemini_2_0.json")

    process_discussions(discussions, system_prompt,    analyze_with_claude, "analyzed_posts/posts_claude_3_5.json")

    process_discussions(discussions, system_prompt,   analyze_with_chatgpt4omini,"analyzed_posts/posts_gpt_4o_mini.json")

    process_discussions(discussions, system_prompt,   analyze_with_chatgpt4o,"analyzed_posts/posts_gpt_4o.json")
