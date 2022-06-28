from datetime import datetime


def get_time():
    print(datetime.now())
    return datetime.now()


def get_day():
    return str(get_time()).split('.')[0]
