import sys
import requests

from kb.nl.collections import SETS
from kb.nl.helpers import etree

SRU_BASEURL = 'http://jsru.kb.nl/sru/sru'
SRU_BASEURL += '?version=1.2&maximumRecords=%i'
SRU_BASEURL += '&operation=searchRetrieve'
SRU_BASEURL += '&startRecord=%i'
SRU_BASEURL += '&recordSchema=%s'
SRU_BASEURL += '&x-collection=%s&query=%s'


class response():
    def __init__(self, records_data, nr_of_records):
        self.records_data = records_data
        self.nr_of_records = nr_of_records

    @property
    def identifiers(self):
        ids = [i.text.split('=')[1] for i in self.records_data.iter() if
               i.tag.endswith('identifier') and
               i.text.find(':') > -1]
        return ids

    @property
    def records(self):
        ns = {'zs': 'http://www.loc.gov/zing/srw/'}
        records_data = self.records_data.xpath("zs:records/zs:record",
                                               namespaces=ns)
        return(records(records_data))


class records():
    nr_of_records = 0

    def __init__(self, record_data):
        self.record_data = []
        for item in record_data:
            self.record_data.append(item)
            self.nr_of_records += 1

    def __iter__(self):
        i = 0
        while i < len(self.record_data):
            self.current_record = self.record_data[i]
            yield record(self.record_data[i])
            i += 1

    def __getitem__(self, i):
        return record(self.record_data[i])

    def __len__(self):
        return self.nr_of_records


class record():
    def __init__(self, record_data):
        self.record_data = record_data

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


class sru():
    DEBUG = False
    collection = False
    maximumrecords = 50
    nr_of_records = 0
    query = ""
    recordschema = False
    sru_collections = SETS
    startrecord = 0

    def __call__(self):
        pass

    def __iter__(self):
        nr_of_records = self.nr_of_records - self.maximumrecords
        while self.startrecord < nr_of_records:
            self.startrecord += self.maximumrecords
            yield self.search(self.query,
                              self.collection,
                              self.startrecord,
                              self.maximumrecords,
                              self.recordschema)

    def search(self, query, collection=False,
               startrecord=1, maximumrecords=50, recordschema=False):

        self.maximumrecords = maximumrecords
        self.query = query
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

        url = SRU_BASEURL % (maximumrecords, startrecord,
                             self.recordschema, self.collection, query)
        if self.DEBUG:
                sys.stdout.write(url)

        r = requests.get(url)

        if not r.status_code == 200:
            raise Exception('Error while getting data from %s' % url)

        records_data = etree.fromstring(r.content)

        nr_of_records = [i.text for i in records_data.iter() if
                         i.tag.endswith('numberOfRecords')][0]
        nr_of_records = int(nr_of_records)

        if nr_of_records > 0:
            return response(records_data, nr_of_records)

        return False
