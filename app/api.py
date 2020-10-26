import requests
from config import API_key


class CreateObj:

    IMAGES_URL = "http://image.tmdb.org/t/p/w185"
    BACKDROPS_URL = "http://image.tmdb.org/t/p/w780"

    def __init__(self, **data):
        for key in data:
            setattr(self, key, data[key])


class TMDB:

    APIKEY = f"?api_key={API_key}"
    BASE_URL = "https://api.themoviedb.org/3"
    LANGUAGE = "&language=en-US"
    PAGES = "&page=1"

    def _request(self, path, path2, item_id, query):

        response = requests.get(
            f"{self.BASE_URL}{path}{item_id}{path2}{self.APIKEY}{self.LANGUAGE}{self.PAGES}{query}"
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


class GetFilms(TMDB):

    paths = {
        "search_film": "/search/movie",
        "popular_films": "/movie/popular",
        "film_details": "/movie/",
        "recommendations": "/recommendations",
        "in_theaters" : "/movie/now_playing",
        "upcoming" : "/movie/upcoming" 
    }

    def popular_films(self):
        path = self.paths.get("popular_films")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)

    def search_films(self, query):
        query = f"&query={query}"
        path = self.paths.get("search_film")
        response = self._request(path=path, path2="", item_id="", query=query)
        response = response["results"]
        return self._process_multiple_items(response)

    def film_details(self, item_id):
        path = self.paths.get("film_details")
        response = self._request(path=path, path2="", item_id=item_id, query="")
        return self._process_by_id(response)

    def film_recommendations(self, item_id):
        path = self.paths.get("film_details")
        path2 = self.paths.get("recommendations")
        response = self._request(path=path, path2=path2, item_id=item_id, query="")
        response = response["results"]
        return self._process_multiple_items(response)

    def upcoming_films(self):
        path = self.paths.get("upcoming")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)

    def films_in_theaters(self):
        path = self.paths.get("in_theaters")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)



class GetSeries(TMDB):

    paths = {
        "search_series": "/search/tv",
        "popular_series": "/tv/popular",
        "series_details": "/tv/",
        "recommendations": "/recommendations",
        "airing_today": "/tv/airing_today",
        "on_the_air": "/tv/on_the_air"
    }

    def popular_series(self):
        path = self.paths.get("popular_series")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)

    def search_series(self, query):
        query += f"&query={query}"
        path = self.paths.get("search_series")
        response = self._request(path=path, path2="", item_id="", query=query)
        response = response["results"]
        return self._process_multiple_items(response)

    def series_details(self, item_id):
        path = self.paths.get("series_details")
        response = self._request(path=path, path2="", item_id=item_id, query="")
        return self._process_by_id(response)


    def series_recommendations(self, item_id):
        path = self.paths.get("series_details")
        path2 = self.paths.get("recommendations")
        response = self._request(path=path, path2=path2, item_id=item_id, query="")
        response = response["results"]
        return self._process_multiple_items(response)


    def series_airing_today(self, item_id):
        path = self.paths.get("airing_today")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)


    def series_on_the_air(self, item_id):
        path = self.paths.get("on_the_air")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)