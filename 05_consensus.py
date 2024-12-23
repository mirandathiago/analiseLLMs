import itertools
import json
import os
import time
from tqdm import tqdm
from llms.gemini_1_5 import analyze_with_gemini_1_5
from llms.gemini_2_0 import analyze_with_gemini_2_0
from llms.claude_3_2_json import analyze_with_claude
from llms.gpt_4o_mini import analyze_with_chatgpt4omini
from llms.gpt_4o import analyze_with_chatgpt4o
from utils.jsonHandler import load_json

def load_system_prompt(filepath):
     # Carregar prompt do sistema
    with open(filepath, "r") as f:
        system_prompt = f.read().strip()
    return system_prompt

folder = "analyzed_posts/zero-shot/"
llm_files = {
    "gemini_1_5": f"{folder}/posts_gemini_1_5.json",
    "gemini_2_0": f"{folder}/posts_gemini_2_0.json",
    "claude_3_2": f"{folder}/posts_claude_3_5.json",
    "gpt_4o_mini": f"{folder}/posts_gpt_4o_mini.json",
    "gpt_4o": f"{folder}/posts_gpt_4o.json",
    "llama": f"{folder}/posts_llama32.json",
}

desempate_functions = {
    "gemini_1_5": analyze_with_gemini_1_5,
    "gemini_2_0": analyze_with_gemini_2_0,
    "claude_3_5": analyze_with_claude,
    "gpt_4o": analyze_with_chatgpt4o,
    "chatgpt4omini": analyze_with_chatgpt4omini
}

system_prompt = load_system_prompt("prompts/system_prompt_consensus.txt")
output_folder = "analyzed_posts/consensus/zero-shot"

def build_consensus(file_llm1, file_llm2, system_prompt, output_file, consensus_function):
    """
    Função para criar consenso entre duas LLMs.  
    Em caso de discordância, utiliza a função de desempate fornecida.  

    Args:
        file_llm1 (str): Caminho para o arquivo JSON da LLM1.
        file_llm2 (str): Caminho para o arquivo JSON da LLM2.
        consensus_function (callable): Função de desempate a ser chamada em caso de discordância.
        output_file (str): Caminho para salvar o JSON de saída.
    """
    # Carregar os dados das duas LLMs
    with open(file_llm1, "r") as f1, open(file_llm2, "r") as f2:
        llm1_data = json.load(f1)
        llm2_data = json.load(f2)

    # Verificar se ambas têm o mesmo número de discussões
    if len(llm1_data) != len(llm2_data):
        raise ValueError("Os arquivos das LLMs possuem quantidades diferentes de discussões.")

    combined_results = []
    requests = 0
    # Iterar pelas discussões
    for discussion_llm1, discussion_llm2 in tqdm(zip(llm1_data, llm2_data), total=len(llm1_data), desc="Building Consensus", unit="Discussion"):
        # Copiar os dados iniciais
        combined_discussion = {**discussion_llm1}
        combined_discussion.update({
            "inclusion_llm1": discussion_llm1["Inclusion"],
            "justification_llm1": discussion_llm1["Justification"],
            "inclusion_llm2": discussion_llm2["Inclusion"],
            "justification_llm2": discussion_llm2["Justification"],
        })

        # Se há consenso
        if discussion_llm1["Inclusion"] == discussion_llm2["Inclusion"]:
            combined_discussion["Inclusion"] = discussion_llm1["Inclusion"]
            combined_discussion["Justification"] = "There was a consensus."
            combined_discussion["Relevance"] = max(
                discussion_llm1["Relevance"],
                discussion_llm2["Relevance"],
                key=lambda x: ["False Positive","Terrible", "Poor", "Fair", "Good", "Excellent"].index(x)
            )
        else:
            print("\nHouve discordância --- LLM sendo Chamada...")
            
            # Caso de discordância, usar a função de desempate
            final_decision = consensus_function(
                discussion_llm1["title"],
                discussion_llm1["body"],
                system_prompt
            )
            print('*****************************')
            print(final_decision)
            combined_discussion["Inclusion"] = final_decision["Inclusion"]
            combined_discussion["Relevance"] = final_decision["Relevance"]
            combined_discussion["Justification"] = final_decision["Justification"]
            requests += 1
            if requests % 5 == 0:
                time.sleep(60)  # Evitar limitação de taxa

        # Adicionar o resultado combinado à lista final
        combined_results.append(combined_discussion)

    # Salvar os resultados no arquivo de saída
    with open(output_file, "w") as f:
        json.dump(combined_results, f, indent=4)

    print(f"Processo de consenso concluído. Resultados salvos em '{output_file}'.")



# Verificar e criar pasta de saída
os.makedirs(output_folder, exist_ok=True)

#llm_combinations = list(itertools.combinations(llm_files.items(), 2))
"""
for (llm1_name, llm1_file), (llm2_name, llm2_file) in llm_combinations:
    print(llm1_name," - ",llm2_name)
    for consensus_name, consensus_function in desempate_functions.items():
        output_file = os.path.join(output_folder, 
                f"consensus_{llm1_name}_{llm2_name}_resolve_{consensus_name}.json" )
        print(f"Building consensus for {llm1_name} and {llm2_name} using {consensus_name}...")
        build_consensus(
                file_llm1=llm1_file,
                file_llm2=llm2_file,
                system_prompt=system_prompt,
                output_file=output_file,
                consensus_function=consensus_function
            )
"""



output_file = os.path.join(output_folder, 
                f"consensus_gemini_1_5_llama_resolve_gpt4omini.json" )
build_consensus(
                file_llm1=llm_files["gemini_1_5"],
                file_llm2=llm_files["llama"],
                system_prompt=system_prompt,
                output_file=output_file,
                consensus_function=desempate_functions["chatgpt4omini"]
            )
