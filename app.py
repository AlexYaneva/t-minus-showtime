from flask import Flask
from flask import render_template, url_for, request, redirect
import requests
import json


app = Flask(__name__)


@app.route('/')

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
	title = request.form['title']
	r = requests.get(f'http://www.omdbapi.com/?t={title}&apikey=b644d0fd')
	json_obj = r.json()

	title = json_obj['Title']
	genre = json_obj['Genre']
	cast = json_obj['Actors']
	img = json_obj['Poster']
	result = f'{title} {genre} {cast}'

	return render_template('results.html', result=result, img=img)



if __name__ == '__main__':
	app.run(debug=True)
