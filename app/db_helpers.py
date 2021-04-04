from app import table
from decimal import Decimal
from app.api import GetFilms, GetSeries
from app.utils import countdown


def create_new_user(email, username):
    tracked_id = 0
    new_user = table.put_item(
                                Item={
                                    "Email": email,
                                    "Tracked_id": tracked_id,
                                    "Username": username
                                                            }
                                                                )


def update_password(email, password_hash):
    tracked_id = 0
    table.update_item(
                        Key={
                            "Email": email,
                            "Tracked_id": tracked_id
                                                    },
                        UpdateExpression="SET Password_hash = :setpass",
                        ExpressionAttributeValues={":setpass": password_hash}
                                                                                )


def get_user(email):
    tracked_id = 0
    db_user_item = table.get_item(
                                    Key={
                                        "Email": email,
                                        "Tracked_id": tracked_id
                                                                }
                                                                    )
    try:
        user = db_user_item["Item"]
    except KeyError:
        return None
    return user



def track(email, tracked_id, tracked_type, title, poster_path):
    table.put_item(
                    Item={
                        "Email": email,
                        "Tracked_id": tracked_id,
                        "Tracked_type": tracked_type,
                        "Title" : title,
                        "Poster_path": poster_path
                                                            }
                                                                )


def untrack(email, tracked_id):
    table.delete_item(
                        Key={
                            "Email": email,
                            "Tracked_id": tracked_id
                                                    }
                                                        )


def get_tracked(email, tracked_type):
    '''
    Get all tracked series or films for a user

    :Params: email
             tracked_type - 'films' or 'series'
    '''
    # query the db for all tracked series/films for a user
    all_tracked = table.query(
                        TableName="Users",
                        KeyConditionExpression="Email = :email",
                        FilterExpression="Tracked_type = :tracked_type",
                        ProjectionExpression="Tracked_id",
                        ExpressionAttributeValues={":tracked_type" : tracked_type, ":email" : email}
                                                                                    )
    all_tracked = all_tracked["Items"]

    # extract the series/films IDs from the db response and add them to a list
    all_tracked_ids = []
    for i in all_tracked:
        tracked_id = i.get('Tracked_id')
        all_tracked_ids.append(int(tracked_id))

    # use the list to generate the async url requests, gather the responses
    # calculate countdowns and add all to a new list
    tracked_items = []
    if tracked_type == 'film':
        films = GetFilms(page=1)
        tracked_films = films.async_film_details(all_tracked_ids)
        for item in tracked_films:
            item["countdown"] = countdown(item["release_date"])
            tracked_items.append(item)

    elif tracked_type == 'series':
        series = GetSeries(page=1)
        tracked_series = series.async_series_details(all_tracked_ids)
        for item in tracked_series:
            if item["next_episode_to_air"]:
                item["countdown"] = countdown(item["next_episode_to_air"]["air_date"])
            else:
                # assign a high number to series with no new episodes so they can be shown last
                item["countdown"] = 1000
            tracked_items.append(item)

    # sort the list by countdown
    return  sorted(tracked_items, key=lambda x: x["countdown"])


def get_all_releasing_tomorrow(tracked_type):
    '''
    Get all films or series accross all users
    GSI
    '''

    # retrieve all tracked from the db
    db_response = table.query(
                            TableName="Users",
                            IndexName= "Tracked",
                            KeyConditionExpression="Tracked_type = :tracked_type",
                            ProjectionExpression="Tracked_id, Email, Title, Poster_path",
                            ExpressionAttributeValues={":tracked_type" : tracked_type}
                                                                                        )
    
    db_response = db_response["Items"]

    # add all id's to a set (eliminates duplicates)
    shows_ids = {int(i["Tracked_id"]) for i in db_response}


    # make the http requests to the tmdb api asynchronously
    # SERIES only for testing
    series_object = GetSeries(page=1)
    tmdb_response = series_object.async_series_details(shows_ids)


    # check which episodes are releasing in 1 day and delete the rest
    for i in tmdb_response:
        if i["next_episode_to_air"]:
            countdwn = countdown(i["next_episode_to_air"]["air_date"])
        else:
            countdwn = 1000 
        if countdwn != 1:
            shows_ids.remove(i["id"])


    # create dict with user emails as the keys and a list of shows they track as the values
    email_dict = {i["Email"] : [] for i in db_response}


    # populate the dict only with details of shows which release in 1 day i.e. only the shows in the shows_id list
    for i in db_response:
        if i["Tracked_id"] in shows_ids:
            email_dict[i["Email"]].append({"id" : int(i["Tracked_id"]), "Title" : i["Title"], "Poster_path" : i["Poster_path"]})

    return email_dict




def update_username(email, tracked=0):
    pass



def delete_user(email):
    '''
    Delete the user record and all tracked records
    '''
    # get_tracked()
    pass

