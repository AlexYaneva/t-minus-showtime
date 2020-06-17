import requests
from config import API_key


class CreateObj:

    IMAGES_URL = "http://image.tmdb.org/t/p/w185"
    BACKDROPS_URL = "http://image.tmdb.org/t/p/w300"

    def __init__(self, **data):
        for key in data:
            setattr(self, key, data[key])


class TMDB:

    APIKEY = f"?api_key={API_key}"
    BASE_URL = "https://api.themoviedb.org/3"
    LANGUAGE = "&language=en-US"
    PAGES = "&page=1"

    def _request(self, path, item_id, query):

        response = requests.get(
            f"{self.BASE_URL}{path}{item_id}{self.APIKEY}{self.LANGUAGE}{self.PAGES}{query}"
        ).json()
        return response

    def _process_by_id(self, response):

        obj = CreateObj(**response)
        if obj.poster_path:
            obj.poster_path = f"{obj.IMAGES_URL}{obj.poster_path}"
        if obj.backdrop_path:
            obj.backdrop_path = f"{obj.BACKDROPS_URL}{obj.backdrop_path}"
        return obj

    def _process_multiple_items(self, response):
        obj_list = []
        for dict_item in response:
            obj = CreateObj(**dict_item)
            if obj.poster_path:
                obj.poster_path = f"{obj.IMAGES_URL}{obj.poster_path}"
                obj_list.append(obj)
        return obj_list


class Films(TMDB):

    paths = {
        "search_film": "/search/movie",
        "popular_films": "/movie/popular",
        "film_details": "/movie/",
    }

    def popular_films(self):
        path = self.paths.get("popular_films")
        response = self._request(path=path, item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)

    def search_films(self, query):
        query = f"&query={query}"
        path = self.paths.get("search_film")
        response = self._request(path=path, item_id="", query=query)
        response = response["results"]
        return self._process_multiple_items(response)

    def film_details(self, item_id):
        path = self.paths.get("film_details")
        response = self._request(path=path, item_id=item_id, query="")
        return self._process_by_id(response)


class Series(TMDB):

    paths = {
        "search_series": "/search/tv",
        "popular_series": "/tv/popular",
        "series_details": "/tv/",
    }

    def popular_series(self):
        path = self.paths.get("popular_series")
        response = self._request(path=path, item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)

    def search_series(self, query):
        query += f"&query={query}"
        path = self.paths.get("search_series")
        response = self._request(path=path, item_id="", query=query)
        response = response["results"]
        return self._process_multiple_items(response)

    def series_details(self, item_id):
        path = self.paths.get("series_details")
        response = self._request(path=path, item_id=item_id, query="")
        return self._process_by_id(response)
