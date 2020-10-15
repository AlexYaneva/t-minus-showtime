from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_caching import Cache
from flask_dynamo import Dynamo
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = "login"
cache = Cache(app)
dynamo = Dynamo(app)
table = dynamo.tables["Users"]
mail = Mail(app)


from app import routes, models, api
