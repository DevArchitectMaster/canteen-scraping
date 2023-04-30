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

    def __del__(self):
        pass
    
    def getScraper(self):
        return self.__scraper_lib
    
    def getEncoding(self):
        return self.__encoding
    
    def getUrl(self):
        return self.__url

    def getHtml(self):
        return self.__html
    
    def openurl(self, url=None, encoding=None):
        if url is not None:
            self.__url = url
        if encoding is not None:
            self.__encoding = encoding

        # selection of the scraper lib
        if self.__scraper_lib == self.__SCRAPER_LIB.URLLIB:
            self.__html = self.__getHtmlByUrllib(self.__url, self.__encoding)
        elif self.__scraper_lib == self.__SCRAPER_LIB.REQUESTS:
            self.__html = self.__getHtmlByRequest(self.__url, self.__encoding)
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

    # docs.python.org/3/library/urllib
    
    def __getHtmlByUrllib(self, url, encoding):
        page = urllib.request.urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode(encoding)
        return html
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      requests methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################

    # requests.readthedocs.io
    
    def __getHtmlByRequest(self, url, encoding):
        response = requests.get(url)
        response.encoding = encoding
        if response.status_code != 200:
            print("Error fetching page")
            exit()
        else:
            html = response.content
        return html