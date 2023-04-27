import os
import pathlib

from utils.database import SQLite as Database
from utils.scraper import Scraper as Scraper

if __name__ == '__main__':
    database_path = str(pathlib.Path("src/database.sqlite3").absolute())
    #url = "https://www.studentenwerk-oberfranken.de/essen/speiseplaene/coburg/hauptmensa.html"
    url = "http://fboeck.de/mensa"
    pattern = ""

    mainCourses_CSS = "div.tx-bwrkspeiseplan__hauptgerichte:nth-child(7) > div:nth-child(1) > div:nth-child(1)"
    mainCourses_CSS = ".tx-bwrkspeiseplan__hauptgerichte > .row > .col-xs-12"
    # table[class*='tx-bwrkspeiseplan__']

    value_scrapling_timestamp = None
    value_intended_date = None
    value_courses_type = None
    value_label = None
    value_ingredients = None
    value_icons = None
    value_price_students = None
    value_price_staff = None
    value_price_guests = None
    value_price_special_fare = None

    #############################################################################################################################################################

    scraper = Scraper(url, pattern)
    html = scraper.gethtml()
    html_mainCourses = scraper.getContentByCSS(mainCourses_CSS)

    #print(html_mainCourses)
    
    #############################################################################################################################################################

    values = (value_scrapling_timestamp, value_intended_date, value_courses_type, value_label, value_ingredients, value_icons, value_price_students, value_price_staff, value_price_guests, value_price_special_fare)
    #temp
    values = ("2022-05-01 12:00:00", "2022-05-02", "entree", "Käsenudeln mit buntem Gemüse", "(2, 16, 17, c, g, i, a1)", "blaetter", 2.40, 3.00, 3.70, 2.60)

    database = Database(database_path)
    #database.init_database()

    id = database.write_scraped_line(values)
    print(id)
    database.close()