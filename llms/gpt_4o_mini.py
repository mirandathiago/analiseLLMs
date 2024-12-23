from dotenv import load_dotenv
import os
import json
from openai import OpenAI


load_dotenv(dotenv_path=".env", override=True)




# Função para processar uma única discussão
def analyze_with_chatgpt4omini(title, body, system_prompt):
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "discussion_analysis_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "Inclusion": {
                        "description": "Indicates if the discussion is included ('Yes' or 'No').",
                        "type": "string",
                        "enum": ["Yes", "No"]
                    },
                    "Relevance": {
                        "description": "Rates the relevance of the discussion.",
                        "type": "string",
                        "enum": ["Excellent", "Good", "Fair", "Poor", "Terrible", "False Positive"]
                    },
                    "Justification": {
                        "description": "Explanation for the decision based on the discussion's content.",
                        "type": "string"
                    }
                },
                "required": ["Inclusion", "Relevance", "Justification"],
                "additionalProperties": False
            }
        }
    }

    developer_prompt = {
        "role": "developer",
        "content": [
            {
                "type": "text",
                "text": system_prompt
            }
        ]
    }
    
    user_prompt = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""
                Title: {title}
                Body: {body}

                Analyze this discussion based on the research protocol and provide the output in JSON with the fields:
                - Inclusion: (Yes/No)
                - Relevance: (Excellent/Good/Fair/Poor/Terrible/False Positive)
                - Justification: (Brief explanation for your decision)
                """
            }
        ]
    }

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_TOKEN")
)
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[developer_prompt,user_prompt ],
            max_tokens=500,
            top_p=1,
            temperature=0.0,  
            response_format=response_format
        )
        
        
        result = response.choices[0].message.content
        
        return json.loads(result)

    except Exception as e:
        print (f"error: {str(e)}")