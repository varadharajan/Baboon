#!/usr/bin/python

# File        : html_parser.py
# Description : Implements a parser to retrieve data from HTML documents

from sgmllib import SGMLParser


class HTMLParser(SGMLParser):
    
    def __init__(self, url):
        SGMLParser.__init__(self)
        self.url = url

    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        import urlparse
        href = [ v for k,v in attrs if k=='href']
        if href:
            currentURL = href.pop()
            parseResult = urlparse.urlparse(currentURL)
            if parseResult.netloc == '' and parseResult.scheme == '':
                currentURL = self.url + currentURL
            self.urls.append(currentURL)
        else:
            pass
