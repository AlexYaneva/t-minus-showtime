from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tracked_films = db.relationship("TrackedFilms", backref="user", lazy="dynamic")
    tracked_series = db.relationship("TrackedSeries", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.user_id

    def trackedfilms(self):
        return self.TrackedFilms.filter(TrackedFilms.user_id == self.user_id)

    def trackedseries(self):
        return self.TrackedSeries.filter(TrackedSeries.user_id == self.user_id)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TrackedFilms(db.Model):
    film_id = db.Column(db.Integer, primary_key=True)
    film_title = db.Column(db.String(140), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def __repr__(self):
        return f"<TrackedFilm {self.film_title}"


class TrackedSeries(db.Model):
    series_id = db.Column(db.Integer, primary_key=True)
    series_title = db.Column(db.String(140), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def __repr__(self):
        return f"<TrackedSeries {self.series_title}"

