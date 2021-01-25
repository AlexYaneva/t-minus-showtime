from app import table, celery
from app.api import GetFilms, GetSeries
from app.utils import countdown

# looks like celery needs the task to return some sort of json and can't return an object instance
# need to solve this somehow... https://stackoverflow.com/questions/49373825/kombu-exceptions-encodeerror-user-is-not-json-serializable

@celery.task
def get_tmdb_series_details(series_id):
    obj = GetSeries(page=1)
    tracked_obj = obj.series_details(item_id=series_id)
    if getattr(tracked_obj, "next_episode_to_air") is not None:
        tracked_obj.countdown = countdown(tracked_obj.next_episode_to_air["air_date"])
    else:
        # assigning a high number to series with no new episodes so they can be shown last
        tracked_obj.countdown = 1000
    return tracked_obj


@celery.task
def get_tmdb_film_details(film_id):
    obj = GetFilms(page=1)
    tracked_obj = obj.film_details(item_id=film_id)
    tracked_obj.countdown = countdown(tracked_obj.release_date)
    return tracked_obj








