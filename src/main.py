import os
import pathlib

from utils.scraper import Scraper as Scraper
from utils.parser import Parser as Parser
from utils.model import CannteenModel as Model
from utils.database import SQLite as Database

##################################################################################################################################
#                                                                                                                                #
#                                                         C O N F I G                                                            #
#                                                                                                                                #
##################################################################################################################################

dataobject = Model()._getModelAsDict()
dataobject.pop("id")

database_path = str(pathlib.Path("src/database.sqlite3").absolute())
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
    # open existing db, if desired & available
    database.importDatabase(database_path)
    # connect database
    database.connect()
    # init database & tables
    #database.init_database()
    # truncate
    #database.truncate_database() # not necessary if the database was initialised in the previous step

    ################### SCRAPER ###################
    # create
    scraper = Scraper()
    # init scraper
    scraper.openurl(url)
    # get HTML content
    html = scraper.getHtml()

    ################### PARSER ####################
    # create
    parser = Parser()
    # init parser
    parser.loadhtml(html)
    # parse html
    parser.parse()









    #################### MODEL ####################
    # create model
    model = Model()
    #print(model) # empty model
    # ...
    # delete model
    #del model
    
    ###############################################
    #                                             #
    #                 C O N F I G                 #
    #                                             #
    ###############################################

    ############# TODO: edit from here ############

    ################# Hauptgerichte ###############

    mainCourses_CSS = "div.tx-bwrkspeiseplan__hauptgerichte:nth-child(7) > div:nth-child(1) > div:nth-child(1)"
    mainCourses_CSS = ".tx-bwrkspeiseplan__hauptgerichte > .row > .col-xs-12"
    # table[class*='tx-bwrkspeiseplan__']

    # select specific html content with css selector
    html_mainCourses = parser.getContentByCSS(mainCourses_CSS)
    #print(html_mainCourses)

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
    model.importModel(dataobject)
    # export model to db
    export_content = model.exportModel()
    # write
    id = database.write_data(sql_statement=export_content)
    print(id)

    #################### Beilagen #################

    ################## Nachspeisen ################

    ################# Snack & Salat ###############

    ##################### Nudeln ##################

    ########### Abendkarte (ab 16:00 Uhr) #########

















    ################# stop editing ################
    
    ###############################################
  
    # close
    database.close()

    exit(0)