from app import app, login, table
from app.api import GetFilms, GetSeries
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt


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

    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.email, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_email = jwt.decode(token, app.config['SECRET_KEY'],
                                algorithms=['HS256'])['reset_password']
        except:
            return
        
        return table.get_item(Key={"Email": user_email})['Item']


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

    def untrack_film(self, film_id):
        table.update_item(
            Key={"Email": self.email},
            UpdateExpression="DELETE Tracked_films :deletefilm",
            ExpressionAttributeValues={":deletefilm" : set([str(film_id)])}
            )


    def untrack_series(self, series_id):
        table.update_item(
            Key={"Email": self.email},
            UpdateExpression="DELETE Tracked_series :deleteseries",
            ExpressionAttributeValues={":deleteseries" : set([str(series_id)])}
            )



    def get_trackedfilms(self):

        response = table.get_item(
            Key={"Email": self.email}, 
            ProjectionExpression="Tracked_films")

        if "Tracked_films" not in response["Item"]:
            return None

        films = response['Item']['Tracked_films']
        obj_list = []
        for i in films:
            obj = GetFilms()
            # calling the tmdb api 
            film_obj = obj.film_details(item_id=i)
            obj_list.append(film_obj)
        sorted_list = sorted(obj_list, key=lambda film: film.release_date)

        return sorted_list




    def get_trackedseries(self):

        response = table.get_item(
            Key={"Email": self.email}, 
            ProjectionExpression="Tracked_series")

        if "Tracked_series" not in response["Item"]:
            return None
        
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
        print("no user found") # change this
    return User(email=user["Email"])
