'''
/ai/llm/setup.py
-> define all LLM related methods
'''

import requests
from dotenv import load_dotenv
import os

load_dotenv()

# ==================================================
# global vars
# ==================================================

MODEL_NAME = 'sql-agent-lastro'
OLLAMA_URL = os.getenv("OLLAMA_URL")

# ==================================================
# methods
# ==================================================

def queryLLM(currentPrompt, previousPrompts):
    # Format previous prompts array into a string
    previousSection = "\n".join(previousPrompts) if previousPrompts else "None"
    formattedPrompt = f"PREVIOUS: {previousSection}\n\nCURRENT: {currentPrompt}"

    #print(formattedPrompt)

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