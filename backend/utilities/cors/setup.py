'''
/utilities/cors/setup.py
-> cors configs
'''

from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# ==================================================
# methods
# ==================================================

def initCors(app):
    allowed = os.getenv("ALLOWED_ORIGINS", "*")
    origins = "*" if allowed == "*" else allowed.split(',')

    CORS(app, 
         resources={r"/*": {"origins": origins}},
         methods=["GET", "POST"],
         allow_headers=["Content-Type", "Authorization"]
    )