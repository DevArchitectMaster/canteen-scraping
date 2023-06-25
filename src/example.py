import os
import pathlib

from utils.logger import Logger as Logger
logger = Logger().set_logger(loggername=__name__ + '.Example').get_logger()

from utils.scraper import Scraper as Scraper
from utils.parser import Parser as Parser
from utils.model import CannteenModel as Model
from utils.database import SQLite as Database

dataobject = Model()._get_model_as_dict()
dataobject.pop("id")

##################################################################################################################################
#                                                                                                                                #
#                                                         C O N F I G                                                            #
#                                                                                                                                #
##################################################################################################################################

database_path = str(pathlib.Path("src/database.sqlite3").absolute())
url = "http://felix-boeck.de"

##################################################################################################################################
#                                                                                                                                #
#                                                          M A I N                                                               #
#                                                                                                                                #
##################################################################################################################################

if __name__ == '__main__':
    
    ##############################################################################################################################
    #                                                                                                                            #
    #                                                    S C R A P E R                                                           #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")
    print("\t\t### S C R A P E R ###\t\t")

    # create scraper
    scraper = Scraper()
    logger.info("create scraper")

    # init scraper
    scraper.open_url(url)
    logger.info("open url: '%s'", url)

    # get HTML content
    html = scraper.get_html()
    #print(html)
    logger.debug("html code: '%s'", html)

    ##############################################################################################################################
    #                                                                                                                            #
    #                                                     P A R S E R                                                            #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")
    print("\t\t### P A R S E R ###\t\t")

    # create parser
    parser = Parser()
    logger.info("create parser")

    # init parser
    parser.load_html(html)
    #print(parser.getHtml())
    logger.info("load html code")

    # parse html
    parser.parse()
    logger.info("parse html code")
    
    ###############################################
    #                                             #
    #                 C O N F I G                 #
    #                                             #
    ###############################################

    ############# TODO: edit from here ############

    # choose selector wisely
    css_selector = "div"

    # select specific html content with css selector
    selected_html = parser.get_content_by_css(css_selector)
    #print(html_mainCourses)

    # fill emtpy vars with content
    # => temporary fill with static text
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

    ################# stop editing ################
    
    ##############################################################################################################################
    #                                                                                                                            #
    #                                                       M O D E L                                                            #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")
    print("\t\t### M O D E L ###\t\t")

    # create model
    model = Model()
    print(model) # empty model
    logger.info("create model: '%s'", model)

    # fill model
    model.import_model(dataobject)
    print(model)
    logger.info("import model: '%s'", model)

    # export model to db
    export_content = model.export_model()
    logger.info("export model to database: '%s'", export_content)

    ##############################################################################################################################
    #                                                                                                                            #
    #                                                   D A T A B A S E                                                          #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")
    print("\t\t### D A T A B A S E ###\t\t")

    # create database
    database = Database()
    logger.info("create database")

    # open existing db, if desired & available
    #database.import_database(database_path)
    #logger.info("import database '%s'", database_path)

    # connect database
    database.connect()
    logger.info("connect database")

    # init database & tables
    database.init_database()
    logger.info("init database")

    # truncate
    #database.truncate_database() # not necessary if the database was initialised in the previous step
    #logger.info("truncate database")

    # write
    id = database.write_data(sql_statement=export_content)
    print(id)
    logger.info("write dataset to database with id='%s'", id)
    
    # read
    datarow = database.read_dataset_by_id(id=id, columns=True)
    print(datarow)
    logger.info("read dataset from database with id='%s' : '%s'", id, datarow)
  
    # close
    database.close()
    logger.debug("close database connection")

    ##############################################################################################################################
    #                                                                                                                            #
    #                                                        E N D                                                               #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")

    exit(0)