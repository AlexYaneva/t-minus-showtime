from app import app
from app.api import API
from app.models import User
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
	if request.form.get('film_title'):
		film_title = request.form['film_title']
		obj = API()
		results = obj.search_film(film_title)
	elif request.form.get('series_title'):
		series_title = request.form['series_title']
		obj = API()
		results = obj.search_series(series_title)

	return render_template('results.html', results=results)


@app.route('/films', methods=['GET', 'POST'])
def films():
	obj = API()
	results = obj.popular_films()
	return render_template('films.html', results=results)


@app.route('/tvseries', methods=['GET', 'POST'])
def tvseries():
	obj = API()
	results = obj.popular_series()
	return render_template('tvseries.html', results=results)



@app.route('/login', methods=['GET', 'POST'])
def login():
	pass
