import google.generativeai as genai
import json
import re
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

# Configurar API
genai.configure(api_key=os.getenv("GEMINI_TOKEN"))



# Função para análise com Gemini
def analyze_with_gemini_2_0(title,body,system_prompt):
    

    # Inicializar o modelo
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction=system_prompt
    )
   
    user_prompt = f"""
    Title: {title}
    Body: {body}

    Analyze this discussion based on the research protocol and provide the output in JSON with the fields:
    - Inclusion: (Yes/No)
    - Relevance: (Excellent/Good/Fair/Poor/Terrible/False Positive)
    - Justification: (Brief explanation for your decision)
    """
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=400,
            temperature=0,
        )
    )
    json_text = response.text.strip()
    json_text = re.sub(r"```json|```", "", json_text).strip()
    return json.loads(json_text)