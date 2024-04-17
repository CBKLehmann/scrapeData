from functions.database import create_table, read_db
from functions.scraping import call_scrape_function
from functions.extra_func import get_time, get_day
from functions.bulk_ms import bulk_ms


if __name__ == '__main__':
    today = get_day()
    bulk_ms(filename="Adressen Plus_Strictly Confidential")
    # create_table()
    # session = call_scrape_function(today=today, dev=False)  # For Production Purposes set dev to False
    get_time()

    # read_db(session=session)
