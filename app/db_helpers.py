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
    Get all films and series accross all users
    GSI
    '''

    response = table.query(
                        IndexName= "Tracked",
                        KeyConditionExpression="Tracked_type = :tracked_type",
                        ProjectionExpression="Tracked_id, Email",
                        ExpressionAttributeValues={":tracked_type" : tracked_type}
                                                                                )
    return response
    # response should be a list of db items - need to process these - likely need to create a new Tracked model class?

def update_username(email, tracked=0):
    pass



def delete_user(email):
    '''
    Delete the user record and all tracked records
    '''
    # get_tracked()
    pass

