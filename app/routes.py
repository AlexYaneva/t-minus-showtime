from app import app
from flask import render_template, url_for, request, redirect
from config import API_key
import requests
import json

base_url = 'https://api.themoviedb.org/3'
images_url = 'http://image.tmdb.org/t/p/w185' #need to do this in config - a function to get the current images url


@app.route('/')

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
	title = request.form['title']
	r = requests.get(f'{base_url}/search/movie?api_key={API_key}&language=en-US&page=1&query={title}&include_adult=false')
	json_obj = r.json()

	film_title = json_obj['results'][0]['title']
	summary = json_obj['results'][0]['overview']
	poster_path = json_obj['results'][0]['poster_path']
	img = f'{images_url}{poster_path}'
	result = f'{film_title} {summary}'

	return render_template('results.html', result=result, img=img)