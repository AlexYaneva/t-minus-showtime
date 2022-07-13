from app import app, login, table
from app.tmdb_api import GetFilms, GetSeries
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
from app.utils import get_country_by_ip
import jwt
import app.db_helpers as db


class User(UserMixin):

    def __init__(self, email):

        self.email = email
        self.username = self.get_username(email)
        self.location = get_country_by_ip()

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    def get_id(self):
        return self.email

    def set_password(self, email, password):
        password_hash = generate_password_hash(password)
        db.update_password(email, password_hash)

    def get_username(self, email):
        user_record = db.get_user(email)
        username = user_record["Username"]
        return username

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.email, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_email = jwt.decode(token, app.config['SECRET_KEY'],
                                    algorithms=['HS256'])['reset_password']
        except:
            return

        return db.get_user(user_email)

    def track_film(self, tracked_id, title, poster_path):
        tracked_type = 'film'
        db.track(self.email, tracked_id, tracked_type, title, poster_path)

    def track_series(self, tracked_id, title, poster_path):
        tracked_type = 'series'
        db.track(self.email, tracked_id, tracked_type, title, poster_path)

    def untrack(self, tracked_id):
        db.untrack(self.email, tracked_id)

    def get_trackedfilms(self):
        tracked_type = 'film'
        tracked_films = db.get_tracked(self.email, tracked_type)
        return tracked_films

    def get_trackedseries(self):
        tracked_type = 'series'
        tracked_series = db.get_tracked(self.email, tracked_type)
        return tracked_series


@login.user_loader
def load_user(email):
    user = db.get_user(email)
    return User(email=user["Email"])
