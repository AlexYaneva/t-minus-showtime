from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


tracked_films = db.Table(
    "tracked_films",
    db.Column("film_id", db.Integer, db.ForeignKey("films.film_id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id")),
)

tracked_series = db.Table(
    "tracked_series",
    db.Column("series_id", db.Integer, db.ForeignKey("series.series_id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id")),
)


class User(UserMixin, db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    films = db.relationship(
        "Films",
        secondary=tracked_films,
        primaryjoin=(tracked_films.c.user_id == user_id),
        backref=db.backref("tracked_films", lazy="dynamic"),
        lazy="dynamic",
    )

    series = db.relationship(
        "Series",
        secondary=tracked_series,
        primaryjoin=(tracked_series.c.user_id == user_id),
        backref=db.backref("tracked_series", lazy="dynamic"),
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def track_film(self, film):
        # the param film here should be an instance of the db model Film()
        self.films.append(film)

    def track_series(self, series):
        self.series.append(series)

    def get_id(self):
        return self.user_id


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Films(db.Model):

    film_id = db.Column(db.Integer, primary_key=True)
    film_title = db.Column(db.String(140))
    user_id = db.Column(
        db.Integer
    )  # unable to delete this column until i get rid of sqlite

    # film_poster= db.Column(db.String(300)) - this should be path_to_poster and posters of tracked films
    # to be stored in the server filesystem
    # release_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Film {self.film_title}"


class Series(db.Model):

    series_id = db.Column(db.Integer, primary_key=True)
    series_title = db.Column(db.String(140))
    user_id = db.Column(
        db.Integer
    )  # unable to delete this column until i get rid of sqlite

    def __repr__(self):
        return f"<Series {self.series_title}"
