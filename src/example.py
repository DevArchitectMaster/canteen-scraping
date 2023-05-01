import os
import pathlib

from utils.scraper import Scraper as Scraper
from utils.parser import Parser as Parser
from utils.model import CannteenModel as Model
from utils.database import SQLite as Database

dataobject = Model()._getModelAsDict()
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

    # init scraper
    scraper.openurl(url)

    # get HTML content
    html = scraper.getHtml()
    #print(html)

    ##############################################################################################################################
    #                                                                                                                            #
    #                                                     P A R S E R                                                            #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")
    print("\t\t### P A R S E R ###\t\t")

    # create parser
    parser = Parser()

    # init parser
    parser.loadhtml(html)
    #print(parser.getHtml())

    # parse html
    parser.parse()
    
    ###############################################
    #                                             #
    #                 C O N F I G                 #
    #                                             #
    ###############################################

    ############# TODO: edit from here ############

    # choose selector wisely
    mainCourses_CSS = "div.tx-bwrkspeiseplan__hauptgerichte:nth-child(7) > div:nth-child(1) > div:nth-child(1)"

    # select specific html content with css selector
    html_mainCourses = parser.getContentByCSS(mainCourses_CSS)
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

    # fill model
    model.importModel(dataobject)
    print(model)

    # export model to db
    export_content = model.exportModel()

    ##############################################################################################################################
    #                                                                                                                            #
    #                                                   D A T A B A S E                                                          #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")
    print("\t\t### D A T A B A S E ###\t\t")

    # create database
    database = Database()

    # open existing db, if desired & available
    #database.importDatabase(database_path)

    # connect database
    database.connect()

    # init database & tables
    database.init_database()

    # truncate
    #database.truncate_database() # not necessary if the database was initialised in the previous step

    # write
    id = database.write_data(sql_statement=export_content)
    print(id)
    
    # read
    datarow = database.readDataSetById(id=id, columns=True)[0]
    print(datarow)
  
    # close
    database.close()

    ##############################################################################################################################
    #                                                                                                                            #
    #                                                        E N D                                                               #
    #                                                                                                                            #
    ##############################################################################################################################

    print("#######################################################################################################################")

    exit(0)