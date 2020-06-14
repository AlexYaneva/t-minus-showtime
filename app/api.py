
import requests
import json
from config import API_key


class Film:

	def __init__(self, item_id, title, overview, poster_path, backdrop_path, release_date):
		self.id = item_id
		self.title = title
		self.overview = overview
		self.poster_path = poster_path
		self.backdrop_path = backdrop_path
		self.release_date = release_date

class Series:

	def __init__(self, item_id, name, overview, poster_path, backdrop_path, last_episode=None, next_episode=None):
		self.id = item_id
		self.name = name
		self.overview = overview
		self.poster_path = poster_path
		self.backdrop_path = backdrop_path
		self.last_episode = last_episode
		self.next_episode = next_episode



class API:


	paths = {'search_film' : '/search/movie?api_key=',
			'search_series' : '/search/tv?api_key=',
			'popular_films' : '/movie/popular?api_key=',
			'popular_series' : '/tv/popular?api_key=',
			'series_details' : '/tv/',
			'film_details' : '/movie/'}


	def __init__(self):

		self.base_url = 'https://api.themoviedb.org/3'
		self.images_url = 'http://image.tmdb.org/t/p/w185'
		self.backdrops_url = 'http://image.tmdb.org/t/p/w300'




	def process_request(self, json_obj):

		'''
		Class method to process the TMDb API responses for 'search' and 'popular' requests.
		It takes in json, creates instances of the Film and Series classes
		and returns a list of objects
		'''

		results = []

		for item in json_obj:
			item_id = item.get('id')
			name = item.get('name') or None
			title = item.get('title') or None
			overview = item.get('overview')
			poster = item.get('poster_path')
			poster_path = f'{self.images_url}{poster}'
			backdrop = item.get('backdrop_path')
			backdrop_path = f'{self.backdrops_url}{backdrop}'
			release_date = item.get('release_date') or None

			if poster:

				if title:

					film_obj = Film(item_id=item_id, title=title, overview=overview, 
									poster_path=poster_path, backdrop_path=backdrop_path, release_date=release_date)
					results.append(film_obj)

				else:

					series_obj = Series(item_id=item_id, name=name, overview=overview, poster_path=poster_path, 
										backdrop_path=backdrop_path)
					results.append(series_obj)

		return results




	def get_series(self, series_title=None):

		'''
		Class method to issue 'popular' and 'search' GET requests to
		the TMDb API. It calls another class method which processes the json
		response and returns a list of objects.
		'''

		if not series_title:

			path = self.paths.get('popular_series')
			req = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&include_adult=false').json()

		else:

			path = self.paths.get('search_series')
			req = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&query={series_title}&include_adult=false').json()

		json_obj = req['results']
		results = self.process_request(json_obj)

		return results





	def get_films(self, film_title=None):

		'''
		Class method to issue the film related GET requests to
		the TMDb API. It calls another class method which processes the json
		response and returns the received list of objects.
		'''

		if not film_title:

			path = self.paths.get('popular_films')
			req = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&include_adult=false').json()

		else:

			path = self.paths.get('search_film')
			req = requests.get(f'{self.base_url}{path}{API_key}&language=en-US&page=1&query={film_title}&include_adult=false').json()

		json_obj = req['results']
		results = self.process_request(json_obj)

		return results




	# def get_series_by_id(self, series_id):

	# 	'''
	# 	Class method  to get series details by id.
	# 	It takes in json, then creates and
	# 	returns the series object.
	# 	'''

	# 	path = self.paths.get('series_details')
	# 	req = requests.get(f'{self.base_url}{path}{series_id}?api_key={API_key}&language=en-US&page=1&include_adult=false').json()

	# 	item_id = req.get('id')
	# 	name = req.get('name')
	# 	overview = req.get('overview')
	# 	poster = req.get('poster_path')
	# 	poster_path = f'{self.images_url}{poster}'
	# 	backdrop = req.get('backdrop_path')
	# 	backdrop_path = f'{self.backdrops_url}{backdrop}'
	# 	last_episode = req.get('last_episode_to_air')
	# 	next_episode = req.get('next_episode_to_air')

	# 	series_obj = Series(item_id=item_id, name=name, overview=overview, poster_path=poster_path, 
	# 						backdrop_path=backdrop_path, last_episode=last_episode, next_episode=next_episode)

	# 	return series_obj

	def get_by_id(self, item_id, title=None):

		'''
		Class method  to get series or film details by id.
		It takes in the id, then creates and
		returns the series or film object.
		'''

		if title:

			path = self.paths.get('film_details')

		else:

			path = self.paths.get('series_details')

		req = requests.get(f'{self.base_url}{path}{item_id}?api_key={API_key}&language=en-US&page=1&include_adult=false').json()
		item_id = req.get('id')
		name = req.get('name') or None
		title = req.get('title') or None
		overview = req.get('overview')
		poster = req.get('poster_path')
		poster_path = f'{self.images_url}{poster}'
		backdrop = req.get('backdrop_path')
		backdrop_path = f'{self.backdrops_url}{backdrop}'
		release_date = req.get('release_date') or None
		last_episode = req.get('last_episode_to_air') or None
		next_episode = req.get('next_episode_to_air') or None

		if title:

			obj = Film(item_id=item_id, title=title, overview=overview, 
						poster_path=poster_path, backdrop_path=backdrop_path, release_date=release_date)

		else:

			obj = Series(item_id=item_id, name=name, overview=overview, poster_path=poster_path, 
							backdrop_path=backdrop_path, last_episode=last_episode, next_episode=next_episode)

		return obj









