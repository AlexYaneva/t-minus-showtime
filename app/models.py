from app import login, table
from app.api import GetFilms, GetSeries
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin):


    def __init__(self, email):

        self.email = email
        self.username = self.get_username(email)


    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


    def get_id(self):
        return self.email


    def set_password(self, password):
        password_hash = generate_password_hash(password)
        table.update_item(
                    Key={"Email": self.email},
                    UpdateExpression="SET password_hash = :setpass",
                    ExpressionAttributeValues={":setpass": password_hash})


    def get_username(self, email):
        response = table.get_item(Key={"Email": email}, ProjectionExpression="Username")
        username = response["Item"]["Username"]
        return username


    def track_film(self, film_id):
        table.update_item(
            Key={"Email": self.email},
            UpdateExpression="ADD Tracked_films :addfilm",
            ExpressionAttributeValues={":addfilm" : set([str(film_id)])}
            )


    def track_series(self, series_id):
        table.update_item(
            Key={"Email": self.email},
            UpdateExpression="ADD Tracked_series :addseries",
            ExpressionAttributeValues={":addseries" : set([str(series_id)])}
            )


    def get_trackedfilms(self):
        response = table.get_item(
            Key={"Email": self.email}, 
            ProjectionExpression="Tracked_films")
        films = response['Item']['Tracked_films']
        obj_list = []
        for i in films:
            obj = GetFilms()
            # calling the tmdb api 
            film_obj = obj.film_details(item_id=i)
            obj_list.append(film_obj)

        return obj_list


    def get_trackedseries(self):
        response = table.get_item(
            Key={"Email": self.email}, 
            ProjectionExpression="Tracked_series")
        series = response['Item']['Tracked_series']
        obj_list = []
        for i in series:
            obj = GetSeries()
            # calling the tmdb api 
            series_obj = obj.series_details(item_id=i)
            obj_list.append(series_obj)

        return obj_list


@login.user_loader
def load_user(email):
    u = table.get_item(Key={"Email": email})
    user = u["Item"]
    if not user:
        print("no user found")
    return User(email=user["Email"])
