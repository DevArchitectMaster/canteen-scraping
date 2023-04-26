import enum

import requests
from urllib.request import urlopen

import re
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class Scraper:
    class __WebLib(enum.Enum):
        URLLIB = "URLLIB"
        REQUESTS = "REQUESTS"

    def __init__(self, url, pattern={}, decoding="utf-8", **kwargs):
        self.__url = url
        self.__pattern = pattern
        self.__decoding = decoding

        self.__weblib = self.__WebLib.URLLIB

        self.__html = self.openurl(self.__url, self.__decoding)
        
    def openurl(self, url=None, decoding=None):
        if url is None:
            url = self.__url
        if decoding is None:
            decoding = self.__decoding

        if self.__weblib == self.__WebLib.URLLIB:
          self.__html = self.gethtmlByUrllib(url, decoding)
        elif self.__weblib == self.__WebLib.REQUESTS:
          self.__html = self.gethtmlByRequest(url, decoding)

        self.__beautifulSoup = BeautifulSoup(self.__html, "html.parser")
        
        return self.__html
    
    def gethtml(self):
        return self.__html
    
    def gethtmlByUrllib(self, url, decoding):
        self.__page = urlopen(url)
        self.__html_bytes = self.__page.read()
        self.__html = self.__html_bytes.decode(decoding)
        return self.__html
    
    def gethtmlByRequest(self, url, decoding):
        response = requests.get(url)
        if response.status_code != 200:
            print("Error fetching page")
            exit()
        else:
            self.__html = response.content
        return self.__html
    
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