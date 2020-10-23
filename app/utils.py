from datetime import date, datetime

def countdown(release):

    base = str(date.today())
    release_d = release
    release_date = datetime.strptime(release_d, "%Y-%m-%d")
    today = datetime.strptime(base, "%Y-%m-%d")

    difference = release_date - today
    countdown = difference.days
    return countdown if countdown > 0 else 'Released'


def order_by_date(obj_list):
    pass