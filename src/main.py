import os
import pathlib

from utils.logger import Logger as Logger
from utils.scraper import Scraper as Scraper
from utils.parser import Parser as Parser
from utils.model import CannteenModel as Model
from utils.database import SQLite as Database

os.chdir(os.getcwd() + ".\src")

##################################################################################################################################
#                                                                                                                                #
#                                                         L O G G E R                                                            #
#                                                                                                                                #
##################################################################################################################################

configfile = "logging.conf.json"
logpath = "logs/"
loggername = "__main__"

logger = Logger().config(configfile=configfile, loggername=loggername, logpath=logpath).get_logger()

##################################################################################################################################
#                                                                                                                                #
#                                                         C O N F I G                                                            #
#                                                                                                                                #
##################################################################################################################################

dataobject = Model()._get_model_as_dict()
dataobject.pop("id")

database_path = "database.sqlite3"
#url = "https://www.studentenwerk-oberfranken.de/essen/speiseplaene/coburg/hauptmensa.html"
url = "http://fboeck.de/mensa"

##################################################################################################################################
#                                                                                                                                #
#                                                          M A I N                                                               #
#                                                                                                                                #
##################################################################################################################################

if __name__ == '__main__':
    ################## DATABASE ###################
    # create database
    database = Database()
    logger.debug("create database")
    # open existing db, if desired & available
    database.import_database(database_path)
    logger.debug("import database '%s'", database_path)
    # connect database
    database.connect()
    logger.debug("connect database")
    # init database & tables
    #database.init_database()
    #logger.debug("init database")
    # truncate
    #database.truncate_database() # not necessary if the database was initialised in the previous step
    #logger.debug("truncate database")

    ################### SCRAPER ###################
    # create
    scraper = Scraper()
    logger.debug("create scraper")
    # init scraper
    scraper.open_url(url)
    logger.debug("open url: '%s'", url)
    # get HTML content
    html = scraper.get_html()
    logger.debug("html code: '%s'", html)

    ################### PARSER ####################
    # create
    parser = Parser()
    logger.debug("create parser")
    # init parser
    parser.load_html(html)
    logger.debug("load html code")
    # parse html
    parser.parse()
    logger.debug("parse html code")









    #################### MODEL ####################
    # create model
    model = Model()
    #print(model) # empty model
    logger.debug("create model: '%s'", model)
    # ...
    # delete model
    #del model
    
    ###############################################
    #                                             #
    #                 C O N F I G                 #
    #                                             #
    ###############################################

    ############# TODO: edit from here ############

    ###################### HTML ###################

    # choose selector wisely
    meals_CSS_Selector = "div.tx-bwrkspeiseplan__hauptgerichte:nth-child(7) > div:nth-child(1) > div:nth-child(1)" # ".tx-bwrkspeiseplan__hauptgerichte > .row > .col-xs-12"
    # table[class*='tx-bwrkspeiseplan__']

    # select specific html content with css selector
    meals_html = parser.get_content_by_css(meals_CSS_Selector)

    # limitation of html
    parser.load_html(meals_html)

    ################# Hauptgerichte ###############

    hauptgerichte_CSS_Selector = "div[class*='tx-bwrkspeiseplan__hauptgerichte']"
    hauptgerichte_html = parser.get_content_by_css(hauptgerichte_CSS_Selector)

    # fill emtpy vars with content
    dataobject["scrapling_timestamp"] = "2022-05-01 12:00:00"
    dataobject["intended_date"] = "2022-05-02"
    dataobject["courses_type"] = "entree"
    dataobject["label"] = "Käsenudeln mit buntem Gemüse"
    dataobject["ingredients"] = "(2, 16, 17, c, g, i, a1)"
    dataobject["icons"] = "blaetter"
    dataobject["price_students"] = 2.40
    dataobject["price_staff"] = 3.00
    dataobject["price_guests"] = 3.70
    dataobject["price_special_fare"] = 2.60

    # fill model
    model.import_model(dataobject)
    # export model to db
    export_content = model.export_model()
    # write
    id = database.write_data(sql_statement=export_content)
    print(id)

    #################### Beilagen #################

    beilagen_CSS_Selector = "div[class*='tx-bwrkspeiseplan__beilagen']"

    ################## Nachspeisen ################

    desserts_CSS_Selector = "div[class*='tx-bwrkspeiseplan__desserts']"

    ################# Snack & Salat ###############

    salatsuppen_CSS_Selector = "div[class*='tx-bwrkspeiseplan__salatsuppen']"

    ##################### Nudeln ##################

    nudeln_CSS_Selector = "div[class*='tx-bwrkspeiseplan__nudeln']"

    ########### Abendkarte (ab 16:00 Uhr) #########

    abendkarte_CSS_Selector = "div[class*='tx-bwrkspeiseplan__abendkarte']"

















    ################# stop editing ################
    
    ###############################################
  
    # close
    database.close()
    logger.debug("close database connection")

    exit(0)