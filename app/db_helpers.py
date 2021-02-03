from app import table
from decimal import Decimal
from app.api import GetFilms, GetSeries
from app.utils import countdown
from app.tasks import get_tmdb_film_details, get_tmdb_series_details


def create_new_user(email, username):
    tracked_id = 0
    new_user = table.put_item(
                            Item={
                                "Email": email,
                                "Tracked_id": tracked_id,
                                "Username": username
                                                    }
                                                        )
    # generate pass hash, and then update_password()


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
        return 'No user found'
    return user



def track(email, tracked_id, tracked_type, countdown):
    if isinstance(countdown, str):
        table.put_item(
                Item={
                    "Email": email,
                    "Tracked_id": tracked_id,
                    "Tracked_type": tracked_type
                                                }
                                                    )
    elif isinstance(countdown, int):
        table.put_item(
                        Item={
                            "Email": email,
                            "Tracked_id": tracked_id,
                            "Tracked_type": tracked_type,
                            "Countdown" : countdown
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
    all_tracked = table.query(
                        TableName="User_table",
                        KeyConditionExpression="Email = :email",
                        FilterExpression="Tracked_type = :tracked_type",
                        ProjectionExpression="Tracked_id",
                        ExpressionAttributeValues={":tracked_type" : tracked_type, ":email" : email}
                                                                                    )
    all_tracked = all_tracked["Items"]

    # extract all the IDs from the db response
    all_tracked_ids = []
    for i in all_tracked:
        tracked_id = i.get('Tracked_id')
        all_tracked_ids.append(int(tracked_id))

    # get film/series details from the tmdb api and add them to a list
    tracked_items = []
    for i in all_tracked_ids:
        if tracked_type == 'film':
            films = GetFilms(page=1)
            itm = films.film_details(i)
            itm["countdown"] = countdown(itm["release_date"])

        elif tracked_type == 'series':
            series = GetSeries(page=1)
            itm = series.series_details(i)
            if itm["next_episode_to_air"]:
                itm["countdown"] = countdown(itm["next_episode_to_air"]["air_date"])
            else:
                # assigning a high number to series with no new episodes so they can be shown last
                itm["countdown"] = 1000

        tracked_items.append(itm)

    # sort the list by countdown
    return  sorted(tracked_items, key=lambda x: x["countdown"])


def get_all_releasing_tomorrow():
    '''
    Get all films and series accross all users
    which have a release date within 1 day
    GSI
    '''
    countdown = 1
    response = table.query(
                        IndexName= "Tracked",
                        KeyConditionExpression="Countdown = :countdown",
                        ProjectionExpression="Tracked_id, Email, Tracked_type",
                        ExpressionAttributeValues={":countdown" : countdown}
                                                                                )
    # response should be a list of db items - need to process these - likely need to create a new Tracked model class?

def update_username(email, tracked=0):
    pass



def delete_user(email):
    '''
    Delete the user record and all tracked records
    '''
    # get_tracked()
    pass

