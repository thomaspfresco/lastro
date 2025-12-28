# /ai/llm/setup.py

import requests
from dotenv import load_dotenv
import os

load_dotenv()

# ==================================================
# global vars
# ==================================================

MODEL_NAME = 'sql-agent-lastro'
OLLAMA_URL = os.getenv("OLLAMA_URL")

MERGE_CONNECTORS = {'e', 'com', 'em', 'de', 'na', 'no', 'do', 'da', 'à', 'ao', 'sem', 'que'}
NOISE_WORDS = {'enganei-me', 'queria', 'dizer', 'são', 'interessantes', 'vamos', 'ver', 'vídeos', 'projetos', 'mostra'}

# ==================================================
# methods
# ==================================================

def process_prompt_for_action(currentPrompt, previousQueries):

    if not previousQueries:
        return 'RESET'
    
    words = currentPrompt.lower().split()
    
    #significant_words = [w for w in words if w not in NOISE_WORDS]
    significant_words = words
    
    if not significant_words:
        return 'MERGE' 

    first_significant_word = significant_words[0]
    
    if first_significant_word in MERGE_CONNECTORS:
        return 'MERGE'
    else:
        return 'RESET'


def queryLLM(currentPrompt, previousQueries):
    action = process_prompt_for_action(currentPrompt, previousQueries)
    
    previousSection = "\n".join(previousQueries) if previousQueries else "None"

    formattedPrompt = (
        f"<ACTION>{action}</ACTION>\n"
        f"<PREV_SQL>{previousSection}</PREV_SQL>\n"
        f"<PROMPT>{currentPrompt}</PROMPT>"
    )

    print(f"DEBUG ACTION: {action}")
    print(f"DEBUG PROMPT INJECTED:\n{formattedPrompt}")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                'model': MODEL_NAME,
                'prompt': formattedPrompt,
                'stream': False,
                'keep_alive': -1,
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['response']
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
            
    except Exception as e:
        raise Exception(f"Failed to generate SQL: {str(e)}")