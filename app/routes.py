from app import app
from app.api import API
from flask import render_template, url_for, request, redirect


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
	title = request.form['title']
	results = API.search_film(title)

	return render_template('results.html', results=results)