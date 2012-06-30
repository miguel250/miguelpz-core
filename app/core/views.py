from flask import Blueprint, Response, request, session, render_template, redirect, flash, url_for
from app.utils import Github
from app.utils import UserAuth
from app.core.models import User

main = Blueprint('core', __name__,template_folder='../templates')
user_auth = UserAuth('core.login')

@main.route('login/')
def login():
    return render_template('core/login.html')

@main.route('login/github')
def github_login():
      github = Github()
      client_id = github.client_id
      endpoint = 'https://github.com/login/oauth/authorize?client_id=%s&scope=user,public_repo,repo,gist'%(client_id)
      return redirect(endpoint, code=307)

@main.route('callback')
def auth_callback():
    type_auth = request.args.get('type')
    login_url = url_for('.login')

    if type_auth == None:
        flash('Authentication type missing')
        return redirect(login_url, code=307)

    if type_auth == 'github':
        code = request.args.get('code')

        if code == None:
            flash('Invalid verification code')
            return redirect(login_url, code=307)
        
        github = Github()
        token = github.access_token(code)

        if 'error' in token:
            flash('An error has occurred: %s' % token['error'])
            return redirect(login_url, code=307)
        elif 'access_token' in token:
            if user_auth.check_or_create(token['access_token'], type_auth):
                return redirect(login_url, code=307)
            else:
                flash('unknow error')
                return redirect(login_url, code=307) 
        else:
            flash('unknow error')
            return redirect(login_url, code=307)
    else:
        flash('Unknown authentication type')
        return redirect(login_url, code=307)