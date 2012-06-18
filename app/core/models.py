import datetime
from app.config import db

class User(db.Document):
    """User model"""
    username =      db.StringField()
    email =         db.StringField()
    job =           db.StringField()
    city =          db.StringField()
    name =          db.StringField()
    github =        db.StringField()
    twitter =       db.StringField()
    linkedin =      db.StringField()
    facebook =      db.StringField()
    github_id =     db.IntField()
    googleplus =    db.StringField()
    foursquare =    db.StringField()
    gravatar_id =    db.StringField()
    personal_web =  db.StringField()
    token_github =  db.StringField()

class Session(db.Document):
    session_id = db.StringField()
    data = db.DictField()
    expires_on = db.DateTimeField()

    meta = {
        'indexes': ['session_id']
    }