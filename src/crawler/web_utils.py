#!/usr/bin/python

# File        : web_utils.py
# Description : Utilities for parsing and retrieving Hyperlinks from HTML Page

import urllib2
import urlparse
import magic

from html_parser import HTMLParser
from hbase_crawl import HBaseCrawlerInterface
from lxml.html.clean import clean_html

class WebPage:
    
    # Constructor
    def __init__(self, targetURL):
        self.url = targetURL
        self.hbaseInterface = HBaseCrawlerInterface()
        
    def removeNonAscii(self,s): 
        return "".join(filter(lambda x: ord(x)<128, s))

    def cleanUpHTML(self, lines):
        self.lines = clean_html(lines)
        self.lines = self.removeNonAscii(self.lines)

    # Retrieve HTML Page and assign it to a variable
    def getHTMLPage(self):
        try:
            if urlparse.urlparse(self.url).scheme == 'http':
                opener = urllib2.build_opener()
                response = urllib2.Request(self.url)
                response.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1')
                lines = opener.open(response).read()
                self.lines = lines
                mime = magic.Magic(mime=True)
                if mime.from_buffer(self.lines) != 'text/html' : raise URLError
                self.cleanUpHTML(self.lines)
            else:
                self.lines = ""
            return self.lines
        except URLError:
            print self.url

    # Retrieves a list of Hyperlinks from the HTML page
    def retrieveHyperLinks(self):
        parser = HTMLParser(self.url)
        parser.feed(self.lines)
        return [ URL for URL in parser.urls 
                 if not self.hbaseInterface.URLExists(URL) ]
    
    # Convert HTML to ASCII/Text
    def getPlainText(self):
        import html2text
        import sys
        try:
            return html2text.html2text(self.lines).split()
        except UnicodeDecodeError:
            pass

    # Generate a word stream for the ASCII/Text document
    def wordStream(self):
        plainText = self.getPlainText()
        if plainText:
            plainText = self.scrapeText(self.removeStopWords(plainText))
            return plainText
        else:
            pass

    # Removes stops words from Plain Text
    def removeStopWords(self, plainText):
        stopWords = open("stopwords", 'r')
        listOfStopWords = [ X.strip() for X in stopWords.readlines() ]
        return [ word.lower() for word in [ X.strip() for X in plainText ] 
                     if word.lower() not in listOfStopWords ]

    # Retrieves only required words
    def scrapeText(self, plainText):
        vocab = open("vocab",'r')
        listofWords = [ X.strip() for X in vocab.readlines() ]
        return [ word for word in [ X for X in plainText ]
                 if word in listofWords ]
        
    def crawlWebPage(self):
        data = {}
        if self.getHTMLPage():
            data['links'] = self.retrieveHyperLinks()
            data['wordstream'] = self.wordStream()
            self.hbaseInterface.insertURL(data['wordstream'], self.url)
            return data['links']
        else:
            pass
