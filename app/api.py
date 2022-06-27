import requests
from config import API_key
from flask import url_for
from flask_login import current_user
from app.utils import async_get_multiple, countdown, convert_date


class TMDB:

    APIKEY = f"?api_key={API_key}"
    IMAGES_URL = "http://image.tmdb.org/t/p/w342"
    LOGOS_URL = "http://image.tmdb.org/t/p/original"
    BACKDROPS_URL = "http://image.tmdb.org/t/p/w780"

    def __init__(self, page):
        self.page = f"&page={page}"
        # should be self.get_base_url().. or should this be a separate task?
        self.base_url = "https://api.themoviedb.org/3"
        self.language = "&language=en-US"

    def _request(self, path, path2, item_id, query, append_to_response):
        ''' method to issue a single http request'''

        response = requests.get(
            f"{self.base_url}{path}{item_id}{path2}{self.APIKEY}{self.language}{self.page}{query}{append_to_response}"
        ).json()
        return response

    def _async_requests(self, path, list_of_ids, append_to_response):
        ''' method to issue multiple http requests asynchronously'''

        urls = []
        for i in list_of_ids:
            url = f"{self.base_url}{path}{i}{self.APIKEY}{self.language}{self.page}{append_to_response}"
            urls.append(url)

        return async_get_multiple(list_of_ids, urls)

    def _process_json_response(self, response):

        for item in response:
            if "poster_path" in item and item["poster_path"] is not None:
                item["poster_path"] = f"{self.IMAGES_URL}{item['poster_path']}"
            else:
                item["poster_path"] = f"{url_for('static', filename='img/no_image.png')}"
            if "next_episode_to_air" in item and item["next_episode_to_air"] is not None:
                if "air_date" in item["next_episode_to_air"] and item["next_episode_to_air"]["air_date"] is not None:
                    item["next_episode_to_air"]['formatted_date'] = convert_date(
                        item["next_episode_to_air"]['air_date'])

            # get release date by country based on current user's location
            if "release_dates" in item:
                results_list = item["release_dates"]["results"]
                country_dict = next(
                    (item for item in results_list if item["iso_3166_1"] == current_user.location["country_code"]), None)
                if country_dict:
                    item['formatted_date'] = convert_date(
                        country_dict["release_dates"][0]["release_date"])

            if "watch/providers" in item:
                try:
                    item["watch/providers"] = item["watch/providers"]["results"][current_user.location["country_code"]]["flatrate"]
                    for i in item["watch/providers"]:
                        i['logo_path'] = f"{self.LOGOS_URL}{i['logo_path']}"
                except KeyError:
                    try:
                        item["watch/providers"] = item["watch/providers"]["results"][current_user.location["country_code"]]["free"]
                        for i in item["watch/providers"]:
                            i['logo_path'] = f"{self.LOGOS_URL}{i['logo_path']}"
                    except KeyError:
                        item["watch/providers"] = None

        return response


class GetFilms(TMDB):

    paths = {
        "search_film": "/search/movie",
        "popular_films": "/movie/popular",
        "film_details": "/movie/",
        "similar": "/similar",
        "in_theatres": "/movie/now_playing",
        "top_rated": "/movie/top_rated"
    }

    def set_countdown(self, item):
        if "formatted_date" in item:
            countdwn = countdown(item["formatted_date"])
        else:
            countdwn = 1000
        return countdwn

    def popular_films(self):
        path = self.paths.get("popular_films")
        response = self._request(
            path=path, path2="", item_id="", query="", append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def search_films(self, query):
        query = f"&query={query}"
        path = self.paths.get("search_film")
        response = self._request(
            path=path, path2="", item_id="", query=query, append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def film_details(self, item_id):
        path = self.paths.get("film_details")
        append_to_response = "&append_to_response=watch/providers,release_dates"
        response = []
        tmdb_req = self._request(
            path=path, path2="", item_id=item_id, query="", append_to_response=append_to_response)
        response.append(tmdb_req)
        return self._process_json_response(response)

    def async_film_details(self, list_of_ids):
        path = self.paths.get("film_details")
        append_to_response = "&append_to_response=watch/providers,release_dates"
        response = self._async_requests(
            path=path, list_of_ids=list_of_ids, append_to_response=append_to_response)
        return self._process_json_response(response)

    def film_recommendations(self, item_id):
        path = self.paths.get("film_details")
        path2 = self.paths.get("similar")
        response = self._request(
            path=path, path2=path2, item_id=item_id, query="", append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def top_rated(self):
        path = self.paths.get("top_rated")
        response = self._request(
            path=path, path2="", item_id="", query="", append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def films_in_theatres(self):
        path = self.paths.get("in_theatres")
        response = self._request(
            path=path, path2="", item_id="", query="", append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def watch_providers(self, item_id):
        path = self.paths.get("film_details")
        path2 = "/watch/providers"
        response = self._request(
            path=path, path2=path2, item_id=item_id, query="", append_to_response="")
        return response


class GetSeries(TMDB):

    paths = {
        "search_series": "/search/tv",
        "popular_series": "/tv/popular",
        "series_details": "/tv/",
        "similar": "/similar",
        "airing_today": "/tv/airing_today",
        "on_the_air": "/tv/on_the_air"
    }

    def set_countdown(self, item):
        if "next_episode_to_air" in item and item["next_episode_to_air"] is not None:
            countdwn = countdown(item["next_episode_to_air"]["air_date"])
        else:
            # assign a high number to series with no new episodes so they can be displayed last
            countdwn = 1000
        return countdwn

    def popular_series(self):
        path = self.paths.get("popular_series")
        response = self._request(
            path=path, path2="", item_id="", query="", append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def search_series(self, query):
        query += f"&query={query}"
        path = self.paths.get("search_series")
        response = self._request(
            path=path, path2="", item_id="", query=query, append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def series_details(self, item_id):
        path = self.paths.get("series_details")
        append_to_response = "&append_to_response=watch/providers,external_ids"
        response = []
        tmdb_req = self._request(
            path=path, path2="", item_id=item_id, query="", append_to_response=append_to_response)
        response.append(tmdb_req)
        return self._process_json_response(response)

    def async_series_details(self, list_of_ids):
        path = self.paths.get("series_details")
        append_to_response = "&append_to_response=watch/providers"
        response = self._async_requests(
            path=path, list_of_ids=list_of_ids, append_to_response=append_to_response)
        return self._process_json_response(response)

    def series_recommendations(self, item_id):
        path = self.paths.get("series_details")
        path2 = self.paths.get("similar")
        response = self._request(
            path=path, path2=path2, item_id=item_id, query="", append_to_response="")
        if "results" in response and response["results"] is not None:
            response = response["results"]
            return self._process_json_response(response)

    def series_airing_today(self):
        path = self.paths.get("airing_today")
        response = self._request(
            path=path, path2="", item_id="", query="", append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def series_on_the_air(self):
        path = self.paths.get("on_the_air")
        response = self._request(
            path=path, path2="", item_id="", query="", append_to_response="")
        response = response["results"]
        return self._process_json_response(response)

    def watch_providers(self, item_id):
        path = self.paths.get("series_details")
        path2 = "/watch/providers"
        response = self._request(
            path=path, path2=path2, item_id=item_id, query="", append_to_response="")
        return response
