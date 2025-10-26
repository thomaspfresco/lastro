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
    CORS(app, 
     origins=os.getenv("ALLOWED_ORIGINS").split(','),
     methods=["GET", "POST"],
     allow_headers=["Content-Type", "Authorization"]
)