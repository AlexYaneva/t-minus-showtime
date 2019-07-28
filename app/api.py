
import requests
import json
from config import API_key


class API:


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
			img = f'{self.images_url}{poster_path}'
			results[img] = item_name

		return results



	def search_film(self, title):
		path = self.paths.get('search_film')
		name = 'title'
		return self.request(path=path, title=title, name=name)


	def search_series(self, title):
		path = self.paths.get('search_series')
		name = 'name'
		return self.request(path=path, title=title, name=name)


	def popular_films(self):
		path = self.paths.get('popular_films')
		name = 'title'
		return self.request(path=path, name=name)

	def popular_series(self):
		path = self.paths.get('popular_series')
		name = 'name'
		return self.request(path=path, name=name)








