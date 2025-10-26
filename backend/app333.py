'''
/app.py
-> main file of the flask app
'''

from flask import Flask, Response, request, jsonify
import json

from database.setup import initDatabase
from database.fetchData import fetchCSV
from database.models import Project

from utilities.scheduler.setup import initScheduler, cleanScheduler
from utilities.cors.setup import initCors

from ai.nlp.setup import initNLP, get_search_engine, refresh_project_embeddings


app = Flask(__name__)

conversation_sessions = {}

# ==================================================
# routes
# ==================================================

@app.route('/')
def home():
    return 'Lastro Backend is running!'

@app.route('/fetch-csv')
def csv():
    return fetchCSV()

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    data = [project.serialize() for project in projects]
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_str, mimetype='application/json; charset=utf-8')

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    json_str = json.dumps(project.serialize(), ensure_ascii=False, indent=2)
    return Response(json_str, mimetype='application/json; charset=utf-8')

# ==================================================
# NLP Chat routes
# ==================================================

@app.route('/chat/<path:prompt>', methods=['GET'])
def chat(prompt):
    """
    NLP-powered chat endpoint for natural language video search
    GET /chat/<prompt>?session_id=xxx&max_results=10
    """
    try:
        session_id = request.args.get('session_id', 'default')
        max_results = int(request.args.get('max_results', 10))
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Get or create conversation session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []
        
        conversation_context = conversation_sessions[session_id]
        
        # Get search engine and perform search
        search_engine = get_search_engine()
        results = search_engine.search(prompt, conversation_context, max_results)
        
        # Store in conversation history
        conversation_sessions[session_id].append({
            'prompt': prompt,
            'results_count': len(results)
        })
        
        # Keep only last 10 interactions
        if len(conversation_sessions[session_id]) > 10:
            conversation_sessions[session_id] = conversation_sessions[session_id][-10:]
        
        # Return results
        json_str = json.dumps({
            'success': True,
            'prompt': prompt,
            'results': results,
            'total_results': len(results),
            'session_id': session_id
        }, ensure_ascii=False, indent=2)
        
        return Response(json_str, mimetype='application/json; charset=utf-8')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/clear', methods=['POST'])
def clear_chat_session():
    """Clear conversation history for a session"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in conversation_sessions:
            del conversation_sessions[session_id]
        
        return jsonify({'success': True, 'message': 'Session cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/refresh', methods=['POST'])
def refresh_embeddings():
    """Refresh NLP embeddings from database"""
    try:
        refresh_project_embeddings()
        return jsonify({'success': True, 'message': 'Embeddings refreshed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    search_engine = get_search_engine()
    return jsonify({
        'status': 'healthy',
        'projects_loaded': len(search_engine.projects_cache) if search_engine else 0
    })

# ==================================================
# main
# ==================================================

if __name__ == '__main__':
    initCors(app)
    initDatabase(app)
    initScheduler(app)

    with app.app_context():
        nlp_engine = initNLP()
        projects = Project.query.all()
        nlp_engine.load_projects(projects)
        print(f"NLP engine loaded with {len(projects)} projects")


    try:
        app.run(debug=True, use_reloader=False)
    finally:
        cleanScheduler()