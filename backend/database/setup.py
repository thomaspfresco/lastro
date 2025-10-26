'''
/database/setup.py
-> database setup
'''

from flask_sqlalchemy import SQLAlchemy
import os

# ==================================================
# global vars
# ==================================================

db = SQLAlchemy()

dbName = 'lastro'

# ==================================================
# initialize and config on app context
# ==================================================

def initDatabase(app):
        dbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), dbName+'.db')
        
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dbPath}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)

        with app.app_context():
            db.create_all()

            from database.models import Project
            from database.fetchData import fetchCSV
            
            if Project.query.count() == 0:
                fetchCSV()
    