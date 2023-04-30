import enum

import requests
from urllib.request import urlopen

NotImplementedErrorMessage = "\n\n\t\t\t### the selected scraper library is not available yet ###\t\t\n\t\t### please select an existing one from the enum '__SCRAPER_LIB' instead ###\t\t\n\n"

class Scraper:
    class __SCRAPER_LIB(enum.Enum):
        URLLIB = "urllib"
        REQUESTS = "requests"

    def __init__(self, url=None, decoding="utf-8", scraper=__SCRAPER_LIB.REQUESTS, **kwargs):
        self.__scraper = scraper
        self.__url = url
        self.__decoding = decoding
        self.__html = None

    def __del__(self):
        pass
    
    def getScraper(self):
        return self.__scraper
    
    def getDecoding(self):
        return self.__decoding
    
    def getUrl(self):
        return self.__url

    def getHtml(self):
        return self.__html
    
    def openurl(self, url=None, decoding=None):
        if url is not None:
            self.__url = url
        if decoding is not None:
            self.__decoding = decoding

        # selection of the scraper lib
        if self.__scraper == self.__SCRAPER_LIB.URLLIB:
            self.__html = self.__getHtmlByUrllib(url, decoding)
        elif self.__scraper == self.__SCRAPER_LIB.REQUESTS:
            self.__html = self.__getHtmlByRequest(url, decoding)
        else:
            raise NotImplementedError(NotImplementedErrorMessage)
            #exit()
        
        return self.__html

    ########################################################   S C R A P E R   #######################################################
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                        urllib methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################
    
    def __getHtmlByUrllib(self, url, decoding):
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode(decoding)
        return html
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      requests methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################
    
    def __getHtmlByRequest(self, url, decoding):
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching page")
            exit()
        else:
            html = response.content
        return html