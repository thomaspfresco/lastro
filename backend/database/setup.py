'''
/database/setup.py
-> database setup
'''

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool
import sqlite3
import os

# ==================================================
# global vars
# ==================================================

db = SQLAlchemy()

dbName = 'lastro.db'
dbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), dbName)

# ==================================================
# initialize and config on app context
# ==================================================

def initDatabase(app):

        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dbPath}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # db pooling protection
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'poolclass': QueuePool,
            'pool_size': 20,
            'max_overflow': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'connect_args': {
                'check_same_thread': False,
                'timeout': 5,
                'uri': True
            }
        }

        db.init_app(app)

        with app.app_context():
            db.create_all()

            from database.models import Project
            from database.fetchData import fetchCSV
            
            if Project.query.count() == 0:
                fetchCSV()

# ==================================================
# other methods
# ==================================================

def getConnection():
    conn = sqlite3.connect(dbPath)
    conn.row_factory = sqlite3.Row
    return conn

def executeQueriesSQL(queries):
    conn = getConnection()
    results = []
    
    try:
        c = conn.cursor()

        for sql in queries:
            c.execute(sql.strip())
            columns = [desc[0] for desc in c.description]
            rows = [dict(zip(columns, row)) for row in c.fetchall()]
            results.append(rows)
        return results
    finally:
        conn.close()

def recordInteraction(data,result):
    if data["cookieConsent"]:
        from database.models import Interaction

        newInteraction = Interaction(
            userInput=data["currentPrompt"],
            userPublicIP=data["userIp"],
            modelOutput=result)

        db.session.add(newInteraction)
        db.session.commit()

        return newInteraction.id