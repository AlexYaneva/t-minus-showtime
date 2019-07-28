
import requests
import json
from config import API_key

# IMAGES_URL = 'http://image.tmdb.org/t/p/w185' # w185 here is my choice of image size
# BASE_URL = 'https://api.themoviedb.org/3'

class API:

	# def api_call(self, main_url, language='&language=en-US', page='&page=1', query=None, include_adult='&include_adult=false'):
	# 	r = requests.get(f'{self.BASE_URL}{main_url}{API_key}{language}{page}{query}{include_adult}')
	# 	json_obj = r.json()

	# 	results = {}
	# 	for film in range(0, len(json_obj['results'])):
	# 		film_title = json_obj['results'][film]['title']
	# 		poster_path = json_obj['results'][film]['poster_path']

	# 		img = f'{self.IMAGES_URL}{poster_path}'
	# 		results[img] = film_title
	# 	return results	

	paths = {'search_film' : '/search/movie?api_key=',
			'search_series' : '/search/tv?api_key=',
			'popular_films' : '/movie/popular?api_key=',
			'popular_series' : '/tv/popular?api_key='}

	def __init__(self):
		self.base_url = 'https://api.themoviedb.org/3'
		self.images_url = 'http://image.tmdb.org/t/p/w185'



	def request(self, path, name, title=None):
		if title:
			r = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&query={title}&include_adult=false')
		else:
			r = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&include_adult=false')
		
		json_obj = r.json()
		results = {}
		for item in range(0, len(json_obj['results'])):
			item_name = json_obj['results'][item][name]
			poster_path = json_obj['results'][item]['poster_path']
			img = f'{IMAGES_URL}{poster_path}'
			results[img] = item_name

		return results




	def search_film(self, title):
		path = self.paths.get('search_film')
		name = 'title'
		self.request(path=path, title=title, name=name)


	def search_series(self, title):
		path = self.paths.get('search_series')
		name = 'name'
		self.request(path=path, title=title, name=name)


	def popular_films(self):
		path = self.paths.get('popular_films')
		name = 'title'
		self.request(path=path, name=name)

	def popular_series(self):
		path = self.paths.get('popular_series')
		name = 'name'
		self.request(path=path, name=name)






	# def search_film(film_title):
	# 	r = requests.get(f'{BASE_URL}/search/movie?api_key={API_key}&language=en-US&page=1&query={film_title}&include_adult=false')
	# 	json_obj = r.json()

	# 	# there could be hundreds of results from a search, for the time being i'm just showing the 1st page
	# 	# need to also extract the film id's and see how to store/render
	# 	results = {}
	# 	for film in range(0, len(json_obj['results'])):
	# 		film_title = json_obj['results'][film]['title']
	# 		poster_path = json_obj['results'][film]['poster_path']

	# 		img = f'{IMAGES_URL}{poster_path}'

	# 		# adding each key-value pair to the results dict
	# 		results[img] = film_title 

	# 	return results


	# def search_series(series_title):
	# 	r = requests.get(f'{BASE_URL}/search/tv?api_key={API_key}&language=en-US&page=1&query={series_title}&include_adult=false')
	# 	json_obj = r.json()

	# 	results = {}
	# 	for series in range(0, len(json_obj['results'])):
	# 		series_title = json_obj['results'][series]['name']
	# 		poster_path = json_obj['results'][series]['poster_path']

	# 		img = f'{IMAGES_URL}{poster_path}'

	# 		results[img] = series_title 

	# 	return results


	# def popular_films():
	# 	r = requests.get(f'{BASE_URL}/movie/popular?api_key={API_key}&language=en-US&page=1&include_adult=false')
	# 	json_obj = r.json()

	# 	results = {}
	# 	for film in range(0, len(json_obj['results'])):
	# 		film_title = json_obj['results'][film]['title']
	# 		poster_path = json_obj['results'][film]['poster_path']

	# 		img = f'{IMAGES_URL}{poster_path}'
	# 		results[img] = film_title

	# 	return results



	# def popular_series():
	# 	r = requests.get(f'{BASE_URL}/tv/popular?api_key={API_key}&language=en-US&page=1&include_adult=false')
	# 	json_obj = r.json()

	# 	results = {}
	# 	for series in range(0, len(json_obj['results'])):
	# 		series_title = json_obj['results'][series]['name']
	# 		poster_path = json_obj['results'][series]['poster_path']

	# 		img = f'{IMAGES_URL}{poster_path}'
	# 		results[img] = series_title

	# 	return results







