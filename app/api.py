
import requests
import json
from config import API_key

images_url = 'http://image.tmdb.org/t/p/w185' # w185 here is my choice of image size
base_url = 'https://api.themoviedb.org/3'

class API():

	def search_film(film_title):
		r = requests.get(f'{base_url}/search/movie?api_key={API_key}&language=en-US&page=1&query={film_title}&include_adult=false')
		json_obj = r.json()

		# there could be hundreds of results from a search, for the time being i'm just showing the first 12
		results = {}
		for film in range(0, 13):
			film_title = json_obj['results'][film]['title']
			poster_path = json_obj['results'][film]['poster_path']

			img = f'{images_url}{poster_path}'

			# adding each key-value pair to the results dict
			results[film_title] = img 

		return results





