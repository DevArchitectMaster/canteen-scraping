from utils.logger import Logger as Logger
logger = Logger().set_logger(loggername=__name__ + '.Parser').get_logger()

import enum

import re
#from html.parser import HTMLParser
import html
import bs4

NotImplementedErrorMessage = "\n\n\t\t\t### the selected parser library is not available yet ###\t\t\n\t\t### please select an existing one from the enum '__PARSER_LIB' instead ###\t\t\n\n"

class Parser:
    class __PARSER_LIB(enum.Enum):
        REGULAR_EXPRESSION = "regular expression"
        HTML_PARSER = "HTMLParser"
        BEAUTIFULSOUP4 = "BeautifulSoup4"

    def __init__(self, html=None, encoding="utf-8", parser=__PARSER_LIB.BEAUTIFULSOUP4, **kwargs):
        self.__parser_lib = parser
        self.__parser = None
        self.__encoding = encoding
        self.__html = html
        logger.debug("Parser Object created")

    def __del__(self):
        pass
    
    def get_parser(self):
        logger.debug("return parser")
        return self.__parser_lib
    
    def get_encoding(self):
        logger.debug("return parser encoding")
        return self.__encoding

    def get_html(self):
        logger.debug("return html code")
        return self.__html
    
    def load_html(self, html=None, encoding=None):
        if html is not None:
            self.__html = html
        if encoding is not None:
            self.__encoding = encoding
        logger.debug("load html code")

        return self.__html
    
    def parse(self):
        # selection of the parser lib
        if self.__parser_lib == self.__PARSER_LIB.REGULAR_EXPRESSION:
            self.__parser = self.__parse_html_by_regular_expression(self.__html, self.__encoding)
        elif self.__parser_lib == self.__PARSER_LIB.HTML_PARSER:
            self.__parser = self.__parse_html_by_html_parser(self.__html, self.__encoding)
        elif self.__parser_lib == self.__PARSER_LIB.BEAUTIFULSOUP4:
            self.__parser = self.__parse_html_by_beautifulsoup(self.__html, self.__encoding)
        else:
            raise NotImplementedError(NotImplementedErrorMessage)
            #exit()
        logger.debug("return parser")
        return self

    def get_content_by_css(self, css_selector):
        logger.debug("get selected content by css selector '%s'", css_selector)
        return self.__parser.select(css_selector)

    ##########################################################   P A R S E R   #######################################################

    # https://requests.readthedocs.io/projects/requests-html/en/latest/
    #TODO: dynamic websit parsing with 'requests-html' or 'selenium'
    
    ##################################################################################################################################
    #                                                                                                                                #
    #                                                  regular expression methods                                                    #
    #                                                                                                                                #
    ##################################################################################################################################

    # docs.python.org/3/library/re

    def __parse_html_by_regular_expression(self, html, encoding):
        #TODO
        parser = None
        logger.debug("parse html code by regex")
        return parser

    """
    def find_all(self, regex_pattern=None):
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

    ##################################################################################################################################
    #                                                                                                                                #
    #                                                    HTMLParser methods                                                          #
    #                                                                                                                                #
    ##################################################################################################################################

    # docs.python.org/3/library/html.parser

    def __parse_html_by_html_parser(self, html, encoding):
        #TODO
        parser = html.parser.HTMLParser()
        parser.feed(html)
        logger.debug("parse html code by html parser")
        return parser

    ##################################################################################################################################
    #                                                                                                                                #
    #                                                   BeautifulSoup methods                                                        #
    #                                                                                                                                #
    ##################################################################################################################################

    # beautiful-soup-4.readthedocs.io

    def __parse_html_by_beautifulsoup(self, html, encoding):
        parser = bs4.BeautifulSoup(html, "html.parser")
        logger.debug("parse html code by beautifulsoup")
        return parser