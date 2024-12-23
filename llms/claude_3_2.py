import os
import json
from tqdm import tqdm
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
        print(response.content[0])
        response_text_cleaned = response.content[0].text.replace("\n", " ")
        last_brace_index = response_text_cleaned.rfind("}")
        if last_brace_index != -1:
            response_text_cleaned = response_text_cleaned[:last_brace_index + 1]
        print(response_text_cleaned)
        print("======================")
        # Extrair e converter a resposta para JSON
        return json.loads(response_text_cleaned)
    
    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"Erro: {str(e)}")
