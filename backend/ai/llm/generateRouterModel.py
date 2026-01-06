'''
/ai/llm/generateModel.py
-> generate Ollama LLM from a base model. define a system prompt and custom parameters
'''

import subprocess
import sys

BASE_MODEL = 'llama3.2:3b'
CUSTOM_MODEL_NAME = 'context-router-lastro'

def create_modelfile():
    modelfile_content = f'''FROM {BASE_MODEL}
PARAMETER temperature 0.0
PARAMETER num_predict 5
PARAMETER num_ctx 1024

SYSTEM """
Detect comparisons in user queries. Output EXACTLY ONE label:

author-equal
author-different
category-equal
category-different
instruments-equal
instruments-different
location-equal
location-different
date-equal
date-different
none-none

EQUALITY indicators:
- parecido, semelhante, igual, mesmo, próximo, mais (when with context)
- With field: "mesmo autor" -> author-equal
- Without field: "vídeos parecidos" or "mais como este" -> category-equal

Location patterns:
- "mais no mesmo sítio" -> location-equal
- "sítio parecido" -> location-equal
- "mais em sítio parecido" -> location-equal
- "outros vídeos neste sítio" -> location-equal
- "mesmo local" or "local próximo" -> location-equal

Instruments patterns:
- "sonoridade parecida" -> instruments-equal
- "timbre parecido" -> instruments-equal
- "instrumentos parecidos" -> instruments-equal

Author patterns:
- "outras obras deste autor" -> author-equal
- "mesmo autor" -> author-equal

DIFFERENCE words (diferente, distinto):
- "autor diferente" -> author-different
- "vídeos completamente diferentes" -> category-different
- "projetos nada a ver (com este)" -> category-different

"outro" alone (without context) means difference:
- "outro autor" -> author-different

No comparison words -> none-none
Examples: "flores", "2011", "carlos", "projetos em lisboa"
"""
'''
    
    with open('Modelfile', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)

# create_modelfile_codellama7b_optimized()
def create_model():    
    try:
        result = subprocess.run(
            ['ollama', 'create', CUSTOM_MODEL_NAME, '-f', 'Modelfile'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Model '{CUSTOM_MODEL_NAME}' created successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: 'ollama' not found. Install from https://ollama.ai")
        sys.exit(1)

def main():
    print("Creating Ollama custom model...\n")
    create_modelfile()
    create_model()

if __name__ == '__main__':
    main()