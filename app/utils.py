import json
import requests
from uuid import uuid4
from config import config
from functools import wraps
from datetime import datetime
from collections import MutableMapping
from app.core.models import Session as Storage
from flask import session, url_for, flash, redirect, request, abort
from flask.sessions import SessionInterface, SessionMixin



class UserAuth(object):
    
    def __init__(self, login_url=None):
        self.session = session
        self.login_url = login_url

    def is_authenticated(self):
        if self.session.get('user_id'):
            return True
        return False

    def is_anonymous(self):
        if self.session.get('user_id'):
            return False
        return True
    
    def get_id(self):
        return self.session.get('user_id')
    
    def get_auth_type(self):
        return self.session.get('auth_type')

    def unauthorized(self):
        flash('You most login to see this page')
        
        if self.login_url:
            login = url_for(self.login_url)
            session['requre_url'] = request.url
            return redirect(login)
        return abort(401)

    def login_required(self,fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not self.is_authenticated():
                return self.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
  

class MongoSession(MutableMapping, SessionMixin):

    def __init__(self, sid, app, *args, **kwargs):
        self.sid = sid
        self.modified = False
        self.conn = None
        storage = Storage.objects(session_id=sid)
        if not storage:
            expires = datetime.utcnow() + app.permanent_session_lifetime
            storage = Storage(session_id=sid, data={}, expires_on=expires)
            storage.save()
            self.new = True

    def __getitem__(self, key):

        rv = None
        storage = Storage.objects(session_id=self.sid).first()

        if key in storage.data:
            rv = storage.data[key]

        if rv is None:
            raise KeyError('Key not in this session')

        return rv

    def __setitem__(self, key, value):

        storage = Storage.objects(session_id=self.sid).first()
        storage.data[key] = value
        storage.save()

        self.modified = True

    def __delitem__(self, key):
        
        storage = Storage.objects(session_id=self.sid).first()
        del  storage.data[key]
        storage.save()

    def __iter__(self):
        storage = Storage.objects(session_id=self.sid).find()

        for key in storage.data.keys():
            yield loads(str(key))

    def __len__(self):
        storage = Storage.objects(session_id=self.sid).first()
        return len(storage)
    
    class CallableAttributeProxy(object):
        def __init__(self, session, key, obj, attr):
            self.session = session
            self.key = key
            self.obj = obj
            self.attr = attr
        def __call__(self, *args, **kwargs):
            rv = self.attr(*args, **kwargs)
            self.session[self.key] = self.obj
            return rv

    class PersistedObjectProxy(object):
        def __init__(self, session, key, obj):
            self.session = session
            self.key = key
            self.obj = obj
        def __getattr__(self, name):
            attr = getattr(self.obj, name)
            if callable(attr):
                return MongoSession.CallableAttributeProxy(
            self.session, self.key, self.obj, attr)
            return attr

    def setdefault(self, key, value):
        if key not in self:
            self[key] = value
            self.modified = True
        return MongoSession.PersistedObjectProxy(
            self, key, self[key])

class MongoSessionInterface(SessionInterface):

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = str(uuid4())
        rv = MongoSession(sid, app)
        return rv

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            storage = Storage.objects(session_id=session.sid)
            storage = storage[0]
            storage.delete()
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                        domain=domain)
            return
        cookie_exp = self.get_expiration_time(app, session)
        response.set_cookie(app.session_cookie_name, session.sid, expires=cookie_exp, httponly=True, domain=domain)

class Github(object):
    """Github api wrapper"""

    AUTH_ENDPOINT = 'https://github.com/login/oauth/access_token'
    HEADERS = {'content-type':'application/json'}

    def __init__(self):
        self.req = requests
        self.secret = config['GITHUB_SECRET']
        self.client_id = config['GITHUB_CLIENTID']

    def access_token(self, code):
       """Get user access token from github """

       payload = json.dumps({
        'client_id':self.client_id, 
        'client_secret':self.secret,
        'code': code,
       })

       response = requests.post(
        self.AUTH_ENDPOINT, 
        data= payload,
        headers=self.HEADERS
        )

       return dict(item.split("=") for item in  response.content.split("&"))