#!/usr/bin/python

# File        : web_utils.py
# Description : Utilities for parsing and retrieving Hyperlinks from HTML Page

import urllib

from html_parser import HTMLParser

class WebPage:
    
    # Constructor
    def __init__(self, targetURL):
        self.url = targetURL
        
    # Retrieve HTML Page and assign it to a variable
    def getHTMLPage(self):
        response = urllib.urlopen(self.url)
        lines = response.read()
        self.lines = lines

    # Retrieves a list of Hyperlinks from the HTML page
    def retrieveHyperLinks(self):
        parser = HTMLParser(self.url)
        parser.feed(self.lines)
        return parser.urls
    
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
        self.getHTMLPage()
        data['links'] = self.retrieveHyperLinks()
        data['wordstream'] = self.wordStream()
        return data
