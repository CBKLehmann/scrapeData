from functions.database import create_table, read_db
from functions.scraping import call_scrape_function
from functions.extra_func import get_time, get_day


if __name__ == '__main__':
    today = get_day()
    create_table()
    session = call_scrape_function(today=today, dev=True)  # For Production Purposes set dev to False
    get_time()

    read_db(session=session)
