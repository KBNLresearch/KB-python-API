import sys
import requests
import urllib

from kb.nl.collections import SETS
from kb.nl.helpers import etree

SRU_BASEURL = 'http://jsru.kb.nl/sru/sru'
SRU_BASEURL += '?version=1.2&maximumRecords=%i'
SRU_BASEURL += '&operation=searchRetrieve'
SRU_BASEURL += '&startRecord=%i'
SRU_BASEURL += '&recordSchema=%s'
SRU_BASEURL += '&x-collection=%s&query=%s'


class response():
    def __init__(self, record_data, sru):
        self.record_data = record_data
        self.sru = sru

    @property
    def identifier(self):
        id = [i.text.split('=')[1] for i in self.record_data.iter() if
              i.tag.endswith('identifier') and
              i.text.find(':') > -1]
        return id[0]

    @property
    def records(self):
        if self.sru.nr_of_records == 0:
            record_data = "<xml></xml>"
        else:
            ns = {'zs': 'http://www.loc.gov/zing/srw/'}
            record_data = self.record_data.xpath("zs:records/zs:record",
                                                 namespaces=ns)[0]
        return(record(record_data, self.sru))

    @property
    def date(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('date')][0]

    @property
    def abstract(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('abstract')][0]

    @property
    def title(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('title')][0]


class record():
    def __init__(self, record_data, sru):
        self.record_data = record_data
        self.sru = sru

    def __iter__(self):
        return self

    def next(self):
        if self.sru.nr_of_records == 0:
            raise StopIteration
        if self.sru.startrecord < self.sru.nr_of_records + 1:
            record_data = self.sru.run_query()
            self.sru.startrecord += 1
            return response(record_data, self.sru)
        else:
            raise StopIteration


class sru():
    DEBUG = False

    collection = False
    maximumrecords = 50
    nr_of_records = 0
    query = ""
    recordschema = False
    sru_collections = SETS
    startrecord = 0

    def search(self, query, collection=False,
               startrecord=1, maximumrecords=1, recordschema=False):

        self.maximumrecords = maximumrecords
        self.query = urllib.quote_plus(query)
        self.startrecord = startrecord

        if collection not in self.sru_collections:
                raise Exception('Unknown collection')

        self.collection = self.sru_collections[collection]['collection']

        if not self.collection:
            raise Exception('Error, no collection specified')

        if not recordschema:
                self.recordschema = self.sru_collections[collection]['recordschema']
        else:
                self.recordschema = recordschema

        record_data = self.run_query()

        nr_of_records = [i.text for i in record_data.iter() if
                         i.tag.endswith('numberOfRecords')][0]

        self.nr_of_records = int(nr_of_records)

        if nr_of_records > 0:
            return response(record_data, self)

        return False

    def run_query(self):
        url = SRU_BASEURL % (self.maximumrecords, self.startrecord,
                             self.recordschema, self.collection, self.query)
        if self.DEBUG:
                sys.stdout.write(url)

        r = requests.get(url)

        if not r.status_code == 200:
            raise Exception('Error while getting data from %s' % url)

        record_data = etree.fromstring(r.content)

        return record_data
