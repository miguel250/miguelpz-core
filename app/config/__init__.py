from flask import Flask
from datetime import timedelta
from flaskext.mongoengine import MongoEngine


class Settings(object):
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = None
    PRESERVE_CONTEXT_ON_EXCEPTION = None
    SECRET_KEY = None
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    USE_X_SENDFILE = False
    LOGGER_NAME = None
    SERVER_NAME = None
    APPLICATION_ROOT = None
    SESSION_COOKIE_NAME = 'miguelpz'
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_HTTPONLY =  True
    SESSION_COOKIE_SECURE =  False
    MAX_CONTENT_LENGTH = None
    SEND_FILE_MAX_AGE_DEFAULT = 12 * 60 * 60
    TRAP_BAD_REQUEST_ERRORS = False
    TRAP_HTTP_EXCEPTIONS =  False
    PREFERRED_URL_SCHEME =  'http'
    MONGODB_DB           =  'MONGODB_DB'
    MONGODB_HOST         = '127.0.0.1'
    
    def __init__(self):
        app = Flask(__name__)
        self.app = app
        self.app.config = {
            'DEBUG':                                self.DEBUG,
            'TESTING':                              self.TESTING,
            'PROPAGATE_EXCEPTIONS':                 self.PROPAGATE_EXCEPTIONS,
            'PRESERVE_CONTEXT_ON_EXCEPTION':        self.PRESERVE_CONTEXT_ON_EXCEPTION,
            'SECRET_KEY':                           self.SECRET_KEY,
            'PERMANENT_SESSION_LIFETIME':           self.PERMANENT_SESSION_LIFETIME,
            'USE_X_SENDFILE':                       self.USE_X_SENDFILE,
            'LOGGER_NAME':                          self.LOGGER_NAME,
            'SERVER_NAME':                          self.SERVER_NAME,
            'APPLICATION_ROOT':                     self.APPLICATION_ROOT,
            'SESSION_COOKIE_NAME':                  self.SESSION_COOKIE_NAME,
            'SESSION_COOKIE_DOMAIN':                self.SESSION_COOKIE_DOMAIN,
            'SESSION_COOKIE_PATH':                  self.SESSION_COOKIE_PATH,
            'SESSION_COOKIE_HTTPONLY':              self.SESSION_COOKIE_HTTPONLY,
            'SESSION_COOKIE_SECURE':                self.SESSION_COOKIE_SECURE,
            'MAX_CONTENT_LENGTH':                   self.MAX_CONTENT_LENGTH,
            'SEND_FILE_MAX_AGE_DEFAULT':            self.SEND_FILE_MAX_AGE_DEFAULT,
            'TRAP_BAD_REQUEST_ERRORS':              self.TRAP_BAD_REQUEST_ERRORS,
            'TRAP_HTTP_EXCEPTIONS':                 self.TRAP_HTTP_EXCEPTIONS,
            'PREFERRED_URL_SCHEME':                 self.PREFERRED_URL_SCHEME,
            'MONGODB_DB':                           self.MONGODB_DB,
            'MONGODB_HOST':                         self.MONGODB_HOST
        }

    def db(self):
        db = MongoEngine(self.app)
        return db

db = Settings().db()