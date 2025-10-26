'''
/app.py
-> main file of the flask app
'''

from flask import Flask, Response, jsonify
import json

from database.setup import initDatabase
from database.fetchData import fetchCSV
from database.models import Project

from utilities.scheduler.setup import initScheduler, cleanScheduler
from utilities.cors.setup import initCors

app = Flask(__name__)

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
    #return jsonify([project.serialize() for project in projects])
    data = [project.serialize() for project in projects]
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(json_str, mimetype='application/json; charset=utf-8')

@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.serialize())
    #json_str = json.dumps(project.serialize(), ensure_ascii=False, indent=2)
    #return Response(json_str, mimetype='application/json; charset=utf-8')


# ==================================================
# main
# ==================================================

if __name__ == '__main__':
    initCors(app)
    initDatabase(app)
    initScheduler(app)

    try:
        app.run(debug=True, use_reloader=False)
    finally:
        cleanScheduler()