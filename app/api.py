# from app import app
import requests
import json
from config import API_key

images_url = 'http://image.tmdb.org/t/p/w185' #w185 here is my choice of image size
base_url = 'https://api.themoviedb.org/3'

class API():

	def search(title):
		r = requests.get(f'{base_url}/search/movie?api_key={API_key}&language=en-US&page=1&query={title}&include_adult=false')
		json_obj = r.json()

		film_title = json_obj['results'][0]['title']
		summary = json_obj['results'][0]['overview']
		poster_path = json_obj['results'][0]['poster_path']
		img = f'{images_url}{poster_path}'
		result = f'{film_title} {summary}'

		return result, img



