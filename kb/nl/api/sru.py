import sys
import requests

from kb.nl.collections import SETS
from kb.nl.helpers import etree

SRU_BASEURL = 'http://services.kb.nl/mdo/oai'


class sru():
    current_set = False
    oai_sets = SETS
    resumptiontoken = False
    DEBUG = False

    def list_sets(self):
        return sorted(self.oai_sets.keys())

    def list_records(self, setname):
        """
           Retrieves a list of records from the OAI server,
           and returns the list of records as an xml object.

           :param setname: OAI setname
        """
        if setname not in self.oai_sets:
            raise ('Error unknown setname')

        if not setname == self.current_set:
            self.current_set = setname
            self.resumptiontoken = False

        url = OAI_BASEURL
        url += '?verb=ListRecords'
        url += '&metadataPrefix=' + self.oai_sets[setname]['metadataPrefix']
        url += '&set=' + self.oai_sets[setname]['setname']

        if self.resumptiontoken:
            url += '&resumptionToken=' + self.resumptiontoken

        if self.DEBUG:
            sys.stdout.write(url)

        response = requests.get(url)

        if not response.status_code == 200:
            raise ('Error while getting data from %s' % url)

        records_data = etree.fromstring(response.text)

        resumptiontoken = [i.text for i in records_data.iter()
                           if i.tag.endswith('resumptionToken')][0]

        self.resumptiontoken = resumptiontoken
        return records(records_data)

    def get(self, identifier):
        """
            Retrieves a record from the OAI server,
            and returns the requested record as an xml object.

            :param identifier: Identifier to get from OAI server
        """
        if self.current_set == "ANP":
            identifier = identifier.split(':')[0] + ':' + identifier
            identifier += ':' + 'mpeg21'
        if self.current_set == 'SGD':
            identifier = identifier.replace('sgd:register', 'SGD:sgd')
            identifier = ":".join(identifier.split(':')[:5])
        if self.current_set == 'DPO':
            identifier = 'DPO:' + identifier
        if self.current_set == 'BYVANCK':
            identifier = 'BYVANCK:' + identifier
            identifier = identifier.replace('BYVANCK', 'ByvanckB')

        url = OAI_BASEURL
        url += '?verb=GetRecord'
        url += '&identifier=' + identifier

        if self.current_set == 'BYVANCK':
            url += '&metadataPrefix=dcx'
        else:
            url += '&metadataPrefix=didl'

        if self.DEBUG:
            sys.stdout.write(url)

        response = requests.get(url)

        if not response.status_code == 200:
            raise ('Error while getting data from %s' % url)

        response = record(etree.fromstring(response.text), self.DEBUG)
        return response


class records():
    """
        Class for parsing xml output from OAI server,
        to more human readable forms. Most notably
        extracts the list of identifiers returned by
        the OAI ListRecords command.
    """
    records_data = False
    DEBUG = False

    def __init__(self, records_data, debug=False):
        self.records_data = records_data

    @property
    def identifiers(self):
        ids = [i.text for i in self.records_data.iter() if
               i.tag.endswith('recordIdentifier') and
               i.text.find(':') > -1]
        return ids


class record():
    """
        Class for parsing XML output from OAI server,
        to more human readable form. This class
        is a generic record level object.
    """
    record_data = False
    DEBUG = False

    def __init__(self, record_data, debug=False):
        """
            :param record_data: XML object of the wanted record.
            :param debug: enable or disable debuging
        """
        self.record_data = record_data

        if debug:
            self.DEBUG = debug

    @property
    def alto(self):
        """
            Return the ALTO for the current record.
            For more information on ALTO see:

            https://en.wikipedia.org/wiki/ALTO_(XML)
        """
        alto_url = False
        for item in self.record_data.iter():
            if item.attrib and \
               item.attrib.get('ref') and \
               item.attrib['ref'].lower().endswith(':alto'):

                alto_url = item.attrib['ref']
                break

        if not alto_url:
            for item in self.record_data.iter():
                if item.attrib and \
                   item.attrib.get('ref') and \
                   item.attrib['ref'].lower().endswith('.xml'):

                    alto_url = item.attrib['ref']
                    break

        if self.DEBUG:
            sys.stdout.write(alto_url)

        response = requests.get(alto_url)

        if not response.status_code == 200:
            raise ('Error while getting data from %s' % alto_url)

        return response.text

    @property
    def image(self):
        """
            Retrieve the image for the current record,
            and return the bytes.
        """
        for item in self.record_data.iter():
            if item.attrib and \
               item.attrib.get('ref') and \
               item.attrib.get('ref').startswith('http://') and \
               (item.attrib['ref'].endswith(':image') or
                    item.attrib['ref'].endswith('.jpg')):

                img_url = item.attrib['ref']
                break

        if self.DEBUG:
            sys.stdout.write(img_url)

        response = requests.get(img_url)

        if not response.status_code == 200:
            raise ('Error while getting data from %s' % img_url)

        return response.text
