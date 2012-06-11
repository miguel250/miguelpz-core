import os
from flask import Flask
from datetime import timedelta
from flaskext.mongoengine import MongoEngine


class Settings(object):
   
    def __init__(self):
        app = Flask(__name__)
        path = os.path.join("../../config/development.cfg")
        app.config.from_pyfile(path)
        self.app = app
    

    def environment(self):
        try:
            root = os.getcwd()
            environment = os.environ['ENVIRONMENT']
            if environment == 'development':
                path = os.path.join(root, "config/development.cfg")
                self.app.config.from_pyfile(path)
            elif environment == 'production':
                path = os.path.join(root, "config/production.cfg")
                self.app.config.from_pyfile(path)
            elif environment == 'testing':
                path = os.path.join(root, "config/testing.cfg")
                self.app.config.from_pyfile(path)
        except KeyError:
            pass

    def db(self):
        self.environment()
        db = MongoEngine(self.app)
        return db

db = Settings().db()