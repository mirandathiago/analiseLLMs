import os
import json
from tqdm import tqdm
import re
from anthropic import Client

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)



# Função para análise com Gemini
def analyze_with_claude(title,body,system_prompt):
    
    # Configurar API
    client = Client(api_key=os.getenv("CLAUDE_TOKEN"))
    user_prompt = f"""
    Title: {title}
    Body: {body}

   Analyze this discussion based on the research protocol and provide the output in JSON with the fields:
    - Inclusion: (Yes/No)
    - Relevance: (Excellent/Good/Fair/Poor/Terrible/False Positive)
    - Justification: (Brief explanation for your decision)
    """
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            temperature=0.0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
       
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```|(\{.*?\})'

        # Procurar o JSON dentro do conteúdo
        json_match = re.search(json_pattern, response.content[0].text, re.DOTALL)

        #print(json_match)

        # Se o padrão for encontrado, processa o JSON
        if json_match:
            json_content = json_match.group(1) or json_match.group(2)
            #json_content = json_match.group(1)  # Captura apenas o conteúdo JSON
            json_content = json_content.replace("\n", " ")

            last_brace_index = json_content.rfind("}")
            if last_brace_index != -1:
              json_content = json_content[:last_brace_index + 1]

        # Extrair e converter a resposta para JSON
        return json.loads(json_content)
    
    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"Erro: {str(e)}")
