import json
import requests
from uuid import uuid4
from config import config
from functools import wraps
from datetime import datetime
from collections import MutableMapping
from app.core.models import Session as Storage, User
from flask import session, url_for, flash, redirect, request, abort
from flask.sessions import SessionInterface, SessionMixin



class UserAuth(object):
    
    def __init__(self, login_url=None):
        self.session = session
        self.login_url = login_url

    def check_or_create(self, token, auth_type):
        if auth_type == 'github':
            github = Github()
            user_info = github.get_user_info(token)
            user = User.objects(github_id=user_info['id']).first()
            
            if not user:
                user = User()
                email_github = github.get_email(token)
                
                user.token_github = token
                user.github = user_info['html_url']
                user.email = email_github[0]
                user.name = user_info['name']
                user.username = user_info['login']
                user.city     = user_info['location']
                user.gravatar_id = user_info['gravatar_id']
                user.github_id =user_info['id']

                user.save()
                self.create_auth_session(user.id, token, auth_type)

            return self.create_auth_session(user.id, token, auth_type)
        else:
            return False

    def create_auth_session(self, user_id, token, auth_type):
        session['user_id'] = user_id
        session['token'] = token
        session['auth_type'] = auth_type

        return self.is_authenticated()

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
        self.storage = Storage.objects(session_id=sid).first()
        if not self.storage:
            expires = datetime.utcnow() + app.permanent_session_lifetime
            self.storage = Storage(session_id=sid, data={}, expires_on=expires)
            self.storage.save()
            self.new = True

    def __getitem__(self, key):

        rv = None
        storage = self.storage
        
        if key in storage.data:
            rv = storage.data[key]

        if rv is None:
            raise KeyError('Key not in this session')

        return rv

    def __setitem__(self, key, value):

        self.storage.data[key] = value
        self.storage.save()

        self.modified = True

    def __delitem__(self, key):

        del  self.storage.data[key]
        self.storage.save()

    def __iter__(self):
        for key in self.storage.data.keys():
            yield str(key)

    def __len__(self):
        
        return len(self.storage)
    
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

    API_END = 'https://api.github.com'
    AUTH_ENDPOINT = 'https://github.com/login/oauth/access_token'
    HEADERS = {'content-type':'application/json'}

    def __init__(self):
        self.req = requests
        self.secret = config['GITHUB_SECRET']
        self.client_id = config['GITHUB_CLIENTID']
    
    def get_email(self, token):
        headers = self.HEADERS
        headers['Authorization'] = 'token %s'%token
        url = '%s/user/emails'%(self.API_END)
        response = requests.get(url, headers=headers)

        return response.json

    def get_limit(self):
        url = '%s/rate_limit'%(self.API_END)
        response = requests.get(url, headers=self.HEADERS)

        return response.json

    def get_user_info(self, token):
        headers = self.HEADERS
        headers['Authorization'] = 'token %s'%token
        url = '%s/user'%(self.API_END)
        response = requests.get(url, headers=headers)

        return response.json

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