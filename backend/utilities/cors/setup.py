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

    if allowed == "*":
        CORS(app,
             resources={r"/*": {
                 "origins": "*",
                 "methods": ["GET", "POST", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": False,
                 "expose_headers": ["Content-Type"],
                 "send_wildcard": True,
                 "always_send": True
             }}
        )
    else:
        origins = allowed.split(',')
        CORS(app,
             resources={r"/*": {
                 "origins": origins,
                 "methods": ["GET", "POST", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True,
                 "always_send": True
             }}
        )