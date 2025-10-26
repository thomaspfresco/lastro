'''
/database/models.py
-> define all the models of the app db
'''

from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Date
from datetime import datetime
from database.setup import db

# -----------------------------
# Custom mutable list of strings
# -----------------------------

class StringList(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, d):
        if value is None:
            return []
        if not isinstance(value, list):
            raise ValueError("Value must be a list of strings")
        return value

    def process_result_value(self, value, d):
        return value or []

# associate MutableList with StringList for change tracking
MutableList.associate_with(StringList)

# -----------------------------
# Project model
# -----------------------------

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)

    link = db.Column(db.String(200), unique=True, nullable=False)
    title = db.Column(db.String(120))
    author = db.Column(db.String(120))
    category = db.Column(StringList, default=list)
    date = db.Column(Date)

    # technical info
    direction = db.Column(StringList, default=list)
    sound = db.Column(StringList, default=list)
    production = db.Column(StringList, default=list)
    support = db.Column(StringList, default=list)
    assistance = db.Column(StringList, default=list)
    research = db.Column(StringList, default=list)

    # geo info
    location = db.Column(db.String(500))

    # instruments
    instruments = db.Column(StringList, default=list)

    # other info
    keywords = db.Column(StringList, default=list)
    infoPool = db.Column(db.String(3000))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "link": self.link,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "date": self.date.isoformat() if self.date else None,

            "direction": self.direction,
            "sound": self.sound,
            "production": self.production,
            "support": self.support,
            "assistance": self.assistance,
            "research": self.research,

            "location": self.location,

            "instruments": self.instruments,

            "keywords": self.keywords,
            "infoPool": self.infoPool,

            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Project {self.id}>'