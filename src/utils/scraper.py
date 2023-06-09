from utils.logger import Logger as Logger
logger = Logger().set_logger(loggername=__name__ + '.Scraper').get_logger()

import enum

import urllib
import requests

NotImplementedErrorMessage = "\n\n\t\t\t### the selected scraper library is not available yet ###\t\t\n\t\t### please select an existing one from the enum '__SCRAPER_LIB' instead ###\t\t\n\n"

class Scraper:
    class __SCRAPER_LIB(enum.Enum):
        URLLIB = "urllib"
        REQUESTS = "requests"

    def __init__(self, url=None, encoding="utf-8", scraper=__SCRAPER_LIB.REQUESTS, **kwargs):
        self.__scraper_lib = scraper
        self.__scraper = None
        self.__url = url
        self.__encoding = encoding
        self.__html = None
        logger.debug("Scraper Object created")

    def __del__(self):
        pass
    
    def get_scraper(self):
        logger.debug("return scraper")
        return self.__scraper_lib
    
    def get_encoding(self):
        logger.debug("return scraper encoding")
        return self.__encoding
    
    def get_url(self):
        logger.debug("return url")
        return self.__url

    def get_html(self):
        logger.debug("return html code")
        return self.__html
    
    def open_url(self, url=None, encoding=None):
        if url is not None:
            self.__url = url
        if encoding is not None:
            self.__encoding = encoding

        # selection of the scraper lib
        if self.__scraper_lib == self.__SCRAPER_LIB.URLLIB:
            self.__html = self.__get_html_by_urllib(self.__url, self.__encoding)
        elif self.__scraper_lib == self.__SCRAPER_LIB.REQUESTS:
            self.__html = self.__get_html_by_request(self.__url, self.__encoding)
        else:
            raise NotImplementedError(NotImplementedErrorMessage)
            #exit()
        
        logger.debug("opened url and return html code")
        return self.__html

    ########################################################   S C R A P E R   #######################################################
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                        urllib methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################

    # docs.python.org/3/library/urllib
    
    def __get_html_by_urllib(self, url, encoding):
        page = urllib.request.urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode(encoding)
        logger.debug("return html code by urllib")
        return html
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      requests methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################

    # requests.readthedocs.io
    
    def __get_html_by_request(self, url, encoding):
        response = requests.get(url)
        response.encoding = encoding
        if response.status_code != 200:
            print("Error fetching page")
            exit()
        else:
            html = response.content
        logger.debug("return html code by request")
        return html