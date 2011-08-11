#!/usr/bin/python

# File        : hbase_crawl.py
# Description : Implements all the necessary utilities to manage crawled data
# TODO        : Hell a lot of things ;)

import sys
import json

# Remove this line
sys.path.append("/Projects/Baboon/lib")

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import *

class HBaseCrawlerInterface:
    def __init__(self):
        self.tableName = "Dataset" # Generalize it using configParser
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = Hbase.Client(protocol)
        transport.open()

    def URLExists(self, url):
        if self.client.getRow(self.tableName, url):
            return True
        else:
            return False

    def insertURL(self, data, url):
        dump = json.dumps(data)
        mutations = [Mutation(column="Profile:content", value=dump)]
        self.client.mutateRow(self.tableName, url, mutations)


