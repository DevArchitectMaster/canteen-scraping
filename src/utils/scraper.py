import enum

import requests
from urllib.request import urlopen

import re
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class Scraper:
    class __SCRAPER_LIB(enum.Enum):
        URLLIB = "urllib"
        REQUESTS = "requests"

    class __PARSER_LIB(enum.Enum):
        REGULAR_EXPRESSION = "regular expression"
        HTML_PARSER = "HTMLParser"
        BEAUTIFULSOUP4 = "BeautifulSoup4"

    def __init__(self, url, decoding="utf-8", scraper=__SCRAPER_LIB.REQUESTS, parser=__PARSER_LIB.HTML_PARSER, **kwargs):
        self.__url = url
        self.__decoding = decoding

        self.__scraper = scraper
        self.__parser = parser

        self.__html = self.openurl(self.__url, self.__decoding)

    def __del__(self):
        pass
        
    def openurl(self, url=None, decoding=None):
        if url is None:
            url = self.__url
        if decoding is None:
            decoding = self.__decoding

        if self.__scraper == self.__SCRAPER_LIB.URLLIB:
          self.__html = self.__gethtmlByUrllib(url, decoding)
        elif self.__scraper == self.__SCRAPER_LIB.REQUESTS:
          self.__html = self.__gethtmlByRequest(url, decoding)
        
        return self.__html
    
    def getScraper(self):
        return self.__scraper
    
    def getParser(self):
        return self.__parser
    
    def getDecoding(self):
        return self.__decoding
    
    def getUrl(self):
        return self.__url

    def getHtml(self):
        return self.__html
    
    def parse(self):
        #TODO
        pass
    


    """
    def findall(self, regex_pattern=None):
        if regex_pattern is None:
            regex_pattern = self.__pattern
        
        return re.findall(regex_pattern, self.__html, re.IGNORECASE)
    """

    """
    def parse(self, regex_pattern=None):
        if regex_pattern is None:
            regex_pattern = self.__pattern
        
        self.__soup = BeautifulSoup(self.__html, "html.parser")
        return self.__soup.find_all_next(regex_pattern)
    """

    def getContentByCSS(self, css_selector):        
        return self.__beautifulSoup.select(css_selector)
    


    ########################################################   S C R A P E R   #######################################################
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                        urllib methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################
    
    def __gethtmlByUrllib(self, url, decoding):
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode(decoding)
        return html
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                      requests methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################
    
    def __gethtmlByRequest(self, url, decoding):
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching page")
            exit()
        else:
            html = response.content
        return html
    
    ##########################################################   P A R S E R   #######################################################

    # https://requests.readthedocs.io/projects/requests-html/en/latest/
    #TODO: dynamic websit parsing with 'requests-html' or 'selenium'
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                  regular expression methods                                                    #
    #                                                                                                                                #
    ##################################################################################################################################

    ##################################################################################################################################
    #                                                                                                                                #
    #                                                   BeautifulSoup methods                                                        #
    #                                                                                                                                #
    ##################################################################################################################################

    ##################################################################################################################################
    #                                                                                                                                #
    #                                                    HTMLParser methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################
    
    pass