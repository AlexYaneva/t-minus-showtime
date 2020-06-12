
import requests
import json
from config import API_key


class Film:

	def __init__(self, item_id, title, overview, poster_path, backdrop_path, release_date, status=None):
		self.id = item_id
		self.title = title
		self.overview = overview
		self.poster_path = poster_path
		self.backdrop_path = backdrop_path
		self.status = status
		self.release_date = release_date

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
			r = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&query={title}&include_adult=false').json()
		else:
			r = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&include_adult=false').json()
		
		json_obj = r['results']
		results = []
		for item in json_obj:
			item_id = item.get('id')
			title = item.get('title')
			overview = item.get('overview')
			poster = item.get('poster_path')
			poster_path = f'{self.images_url}{poster}'
			backdrop = item.get('backdrop_path')
			release_date = item.get('release_date')
			
			film_obj = Film(item_id, title, overview, poster_path, backdrop, release_date)
			results.append(film_obj)
			

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











