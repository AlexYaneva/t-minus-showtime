from app import app
from app.api import API
from flask import render_template, url_for, request, redirect


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
	if request.form['film_title']:
		film_title = request.form['film_title']
		results = API.search_film(film_title)
	elif request.form['series_title']:
		series_title = request.form['series_title']
		results = API.search_series(series_title)

	return render_template('results.html', results=results)


@app.route('/films', methods=['GET', 'POST'])
def films():
	results = API.popular_films()
	return render_template('films.html', results=results)


@app.route('/tvseries', methods=['GET', 'POST'])
def tvseries():
	results = API.popular_series()
	return render_template('tvseries.html', results=results)