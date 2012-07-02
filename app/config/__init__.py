import os
from flask import Flask
from datetime import timedelta
from flaskext.mail import Mail
from flask.ext.mongoengine import MongoEngine


class Settings(object):
   
    def __init__(self):
        app = Flask(__name__)
        path = os.path.join("../../config/base.cfg")
        app.config.from_pyfile(path)
        self.app = app
        self.environment()
    
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

    def App(self):
        return self.app
    def config(self):
        return self.app.config

    def db(self):
        db = MongoEngine(self.app)
        return db

settings = Settings()
db = settings.db()
config = settings.config()
mail = Mail(settings.App())