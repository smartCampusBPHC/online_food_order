from flask import Flask
from flask_admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
admin = Admin(app, template_mode='bootstrap3')
app.config.from_object('config')
db = SQLAlchemy(app)

import ancapp.views, ancapp.models, ancapp.admin
