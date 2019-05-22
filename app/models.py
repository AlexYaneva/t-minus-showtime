from app import db

class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tracked_films = db.relationship('TrackedFilms', lazy='dynamic')
	tracked_series = db.relationship('TrackedSeries', lazy='dynamic')

	def __repr__(self):
		return f'<User {self.username}>' 


class TrackedFilms(db.Model):
	film_id = db.Column(db.Integer, primary_key=True)
	film_title = db.Column(db.String(140), index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

	def __repr__(self):
		return f'<TrackedFilm {self.film_title}'


class TrackedSeries(db.Model):
	series_id = db.Column(db.Integer, primary_key=True)
	series_title = db.Column(db.String(140), index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

	def __repr__(self):
		return f'<TrackedSeries {self.series_title}'