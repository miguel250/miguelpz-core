from app.config import db

class User(db.Document):
    """User model"""
    username =      db.StringField(required=True)
    email =         db.StringField(required=True)
    job =           db.StringField(required=True)
    city =          db.StringField(required=True)
    name =          db.StringField(required=True)
    github =        db.StringField(required=True)
    twitter =       db.StringField(required=True)
    linkedin =      db.StringField(required=True)
    facebook =      db.StringField(required=True)
    googleplus =    db.StringField(required=True)
    foursquare =    db.StringField(required=True)
    personal_web =  db.StringField(required=True)