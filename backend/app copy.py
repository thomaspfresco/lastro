'''
/app.py
-> main file of the flask app
'''

from flask import Flask, Response
import json

from database.setup import initDatabase
from database.fetchData import fetchCSV
from database.models import Project

from utilities.scheduler.setup import initScheduler, cleanScheduler


from flask import Flask, request, jsonify
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

CATEGORIES = [
    "Artesanato", "Dança", "Comida", "Histórias", "Música", 
    "Tradição Oral", "Poesia", "Práticas de Religião e Ritos", "Paisagens Sonoras"
]

print("Loading AI model...")
classifier = pipeline("zero-shot-classification", model="neuralmind/bert-base-portuguese-cased")
print("Model loaded!")

# ==================================================
# initialize app
# ==================================================

app = Flask(__name__)

# ==================================================
# routes
# ==================================================

@app.route('/categorize', methods=['GET', 'POST'])
def categorize():
    """Categorize text with smart multi-category filtering"""
    
    # Get parameters
    if request.method == 'GET':
        text = request.args.get('text', '').strip()
        threshold = float(request.args.get('threshold', 0.4))
        max_categories = int(request.args.get('max_categories', 2))
    else:
        data = request.get_json() or {}
        text = data.get('text', '').strip()
        threshold = float(data.get('threshold', 0.4))
        max_categories = int(data.get('max_categories', 2))
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    # AI classification
    result = classifier(text, CATEGORIES)
    
    # Smart filtering logic
    filtered_categories = []
    
    for i, (category, score) in enumerate(zip(result['labels'], result['scores'])):
        if score >= threshold:
            # Include if above threshold
            filtered_categories.append({'category': category, 'score': round(score, 3)})
        elif i == 0 and score >= 0.08:
            # Always include top category if at least 8%
            filtered_categories.append({'category': category, 'score': round(score, 3)})
        elif len(filtered_categories) == 1 and i == 1 and score >= (filtered_categories[0]['score'] * 0.6):
            # Include second if it's 60%+ of first (handles "Música para dança" cases)
            filtered_categories.append({'category': category, 'score': round(score, 3)})
    
    # Limit results
    filtered_categories = filtered_categories[:max_categories]
    categories = [item['category'] for item in filtered_categories]
    
    return jsonify({
        'text': text,
        'categories': categories
    })

@app.route('/')
def home():
    return 'Lastro Backend is running!'

@app.route('/update-data')
def csv():
    return fetchCSV()

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    data = [project.serialize() for project in projects]
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_str, mimetype='application/json; charset=utf-8')

# ==================================================
# main
# ==================================================

if __name__ == '__main__':
    initDatabase(app)
    initScheduler(app)
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        cleanScheduler()