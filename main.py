from functions.database import create_table, read_db
from functions.scraping import call_scrape_function
from functions.extra_func import get_time, get_day
from functions.json_func import edit_data_json


if __name__ == '__main__':
    today = get_day()
    create_table()
    session, data_arr = call_scrape_function(today=today, dev=True)  # For Development Purposes set dev to False
    edit_data_json(data_arr=data_arr, today=today)
    get_time()

    read_db(session=session)
