
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_caching import Cache
from flask_dynamo import Dynamo
from flask_mail import Mail
from celery import Celery

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = "login"
cache = Cache(app)
dynamo = Dynamo(app)
table = dynamo.tables["User_table"]
mail = Mail(app)
celery = Celery(app.import_name,
                backend=app.config['CELERY_RESULT_BACKEND'],
                broker=app.config['CELERY_BROKER_URL'])


from app import routes, models, tmdb_api

