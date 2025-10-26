'''
/utilities/vimeo/setup.py
-> handle vimeo api communications
'''

from dotenv import load_dotenv
from datetime import datetime
import requests
import os

load_dotenv()

# ==================================================
# global vars
# ==================================================

# vimeo token for publish dates fetch
VIMEO_TOKEN = os.getenv("VIMEO_TOKEN")

# ==================================================
# methods
# ==================================================

def getVimeoDate(pid):
    url = f"https://api.vimeo.com/videos/{pid}"
    headers = {
        "Authorization": f"bearer {VIMEO_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        dt = datetime.fromisoformat(data.get("created_time").replace("Z", "+00:00"))
        return dt.date()
    elif response.status_code == 429: # Rate limit exceeded
        print("Vimeo API rate limit exceeded — 429")
        return "RATE_LIMIT_EXCEEDED"
    else:
        print("Error:", response.json())
        return f"{response.json()}"