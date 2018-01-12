import sys
import requests
import urllib
import pprint

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

from kb.nl.collections import SETS
from kb.nl.helpers import etree

SRU_BASEURL = 'https://jsru.kb.nl/sru/sru'
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
    def records(self):
        if self.sru.nr_of_records == 0:
            record_data = "<xml></xml>"
        else:
            ns = {'zs': 'http://www.loc.gov/zing/srw/'}
            record_data = self.record_data.xpath("zs:records/zs:record",
                                                 namespaces=ns)[0]
        return(record(record_data, self.sru))

    # TODO: distinguish by xsi:type
    @property
    def identifiers(self):
        baseurl = 'https://resolver.kb.nl/resolve?urn='
        result = [r.text.replace(baseurl, '') for r in self.record_data.iter() if
                  r.tag.endswith('identifier') and r.text.find(':') > -1]
        return result

    @property
    def types(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('type')]

    @property
    def languages(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('language')]

    @property
    def dates(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('date')]

    @property
    def extents(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('extent')]

    @property
    def creators(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('creator')]

    @property
    def contributors(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('contributor')]

    # TODO: distinguish by xsi:type and xml:lang
    @property
    def subjects(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('subject')]

    @property
    def abstracts(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('abstract')]

    @property
    def titles(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('title')]

    @property
    def publishers(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('publisher')]

    # Following properties occur in GGC

    @property
    def annotations(self):
        return [r.text for r in self.record_data.iter() if
                r.tag.endswith('annotation')]


class record():
    def __init__(self, record_data, sru):
        self.record_data = record_data
        self.sru = sru

    def __iter__(self):
        return self

    def __next__(self):
        if self.sru.nr_of_records == 0:
            raise StopIteration
        if self.sru.startrecord < self.sru.nr_of_records + 1:
            record_data = self.sru.run_query()
            self.sru.startrecord += 1
            return response(record_data, self.sru)
        else:
            raise StopIteration

    def next(self):
        return self.__next__()


class sru():
    DEBUG = True

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
        self.query = quote(query)
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

        if self.nr_of_records > 0:
            return response(record_data, self)

        return False

    def run_query(self):
        url = SRU_BASEURL % (self.maximumrecords, self.startrecord,
                             self.recordschema, self.collection, self.query)
        if self.DEBUG:
            print("run_query: %s" % url)

        r = requests.get(url)

        if not r.status_code == 200:
            raise Exception('Error while getting data from %s' % url)

        record_data = etree.fromstring(r.content)

        return record_data
