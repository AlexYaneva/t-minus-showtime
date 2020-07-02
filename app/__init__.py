from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from flask_dynamo import Dynamo

app = Flask(__name__)
app.config.from_object(Config)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
cache = Cache(app)
dynamo = Dynamo(app)
table = dynamo.tables["Users"]

from app import routes, models, api
