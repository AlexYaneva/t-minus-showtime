import requests
from config import API_key
from app.utils import async_get_multiple


class TMDB:

    APIKEY = f"?api_key={API_key}"
    IMAGES_URL = "http://image.tmdb.org/t/p/w185"
    BACKDROPS_URL = "http://image.tmdb.org/t/p/w780" 

    def __init__(self, page):
        self.page = f"&page={page}"
        self.base_url = "https://api.themoviedb.org/3" #  should be self.get_base_url().. or should this be a separate task?
        self.language = "&language=en-US"


    def _request(self, path, path2, item_id, query):

        response = requests.get(
            f"{self.base_url}{path}{item_id}{path2}{self.APIKEY}{self.language}{self.page}{query}"
        ).json()
        return response



    def _async_requests(self, path, list_of_ids):
        urls = []
        for i in list_of_ids:
            url = f"{self.base_url}{path}{i}{self.APIKEY}{self.language}{self.page}"
            urls.append(url)
            
        return async_get_multiple(list_of_ids, urls)



    def _process_by_id(self, response):

        if "poster_path" in response:
            response["poster_path"] = f"{self.IMAGES_URL}{response['poster_path']}"
        if "backdrop_path" in response:
            response["backdrop_path"] = f"{self.BACKDROPS_URL}{response['backdrop_path']}"
        return response


    def _process_multiple_items(self, response):

        for item in response:
            if item["poster_path"]:
                item["poster_path"] = f"{self.IMAGES_URL}{item['poster_path']}"
        return response


class GetFilms(TMDB):

    paths = {
        "search_film": "/search/movie",
        "popular_films": "/movie/popular",
        "film_details": "/movie/",
        "similar": "/similar",
        "in_theatres" : "/movie/now_playing",
        "top_rated" : "/movie/top_rated" 
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


    def async_film_details(self, list_of_ids):
        path = self.paths.get("film_details")
        response = self._async_requests(path=path, list_of_ids=list_of_ids)
        return self._process_multiple_items(response)



    def film_recommendations(self, item_id):
        path = self.paths.get("film_details")
        path2 = self.paths.get("similar")
        response = self._request(path=path, path2=path2, item_id=item_id, query="")
        response = response["results"]
        return self._process_multiple_items(response)


    def top_rated(self):
        path = self.paths.get("top_rated")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)


    def films_in_theatres(self):
        path = self.paths.get("in_theatres")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)



class GetSeries(TMDB):

    paths = {
        "search_series": "/search/tv",
        "popular_series": "/tv/popular",
        "series_details": "/tv/",
        "similar": "/similar",
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

    def async_series_details(self, list_of_ids):
        path = self.paths.get("series_details")
        response = self._async_requests(path=path, list_of_ids=list_of_ids)
        return self._process_multiple_items(response)


    def series_recommendations(self, item_id):
        path = self.paths.get("series_details")
        path2 = self.paths.get("similar")
        response = self._request(path=path, path2=path2, item_id=item_id, query="")
        response = response["results"]
        return self._process_multiple_items(response)


    def series_airing_today(self):
        path = self.paths.get("airing_today")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)


    def series_on_the_air(self):
        path = self.paths.get("on_the_air")
        response = self._request(path=path, path2="", item_id="", query="")
        response = response["results"]
        return self._process_multiple_items(response)