from ancapp import app, db
from flask import Flask, render_template, url_for,jsonify, request, redirect, session, g
from flask_oauthlib.client import OAuth
from .models import User
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required

lm =  LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    if current_user is not None and current_user.is_authenticated:
        return "Logged in as: " + current_user.name
    else:
        return "Log in"

@app.route('/user_info')
@login_required
def user_info():
    return "Welcome " + current_user.name


@app.route('/login')
def login():
    if not current_user.is_authenticated:
        return google.authorize(callback=url_for('authorized', _external=True))
    redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    user = User.query.filter_by(google_id = me.data['id']).first()
    if not user:
        user = User()
        user.google_id = me.data['id']
        user.name = me.data['name']
        user.email =  me.data['email']
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
