import sys
import requests

from kb.nl.collections import SETS
from kb.nl.helpers import etree

OAI_BASEURL = 'http://services.kb.nl/mdo/oai'


class oai():
    """
        OAI interface to the National Library of the Netherlands.
        For more information on the OAI protocol, visit:
        http://www.openarchives.org/OAI/openarchivesprotocol.html

        This specific implementation does not strafe to implement a
        perfect OAI client. However it does expose collectionm data from the
        National Library of the Netherlands in Pyhton for easy usage.

        Example usage:

        from kb.nl.api import oai
        from kb.nl.helpers import alto_to_text

        records = oai.list_records("DPO")
        record = oai.get(records.identifiers[0])
        alto_records = record.alto

        for alto_record in alto_records:
            print(alto_to_text(alto_record))

    """
    current_set = False
    oai_sets = SETS
    resumptiontoken = False
    DEBUG = False

    def __init__(self, current_set = False):
        if current_set:
            self.current_set = current_set

    def list_sets(self):
        """
            Shows a list of pre-defined OAI-sets.
        """
        return sorted(self.oai_sets.keys())

    def list_records(self, setname):
        """
           Retrieves a list of records from the OAI server,
           and returns the list of records as an xml object.

           :param setname: OAI setname
        """
        if setname not in self.oai_sets:
            raise Exception('Error unknown setname')

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
            raise Exception('Error while getting data from %s' % url)

        records_data = etree.fromstring(response.content)

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
            identifier = identifier.replace(':mpeg21', '')
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
            raise Exception('Error while getting data from %s' % url)

        response = record(etree.fromstring(response.content),
                          self.current_set, self.DEBUG)
        return response


class records():
    """
        Class for parsing xml output from OAI server,
        to usable objects.
    """
    records_data = False
    DEBUG = False

    def __init__(self, records_data, debug=False):
        """
            :param records_data: ElementTree object
            :param debug: Shows debugging info
        """
        self.records_data = records_data

    @property
    def identifiers(self):
        """
            Return a list of record Identifiers.
        """
        ids = [i.text for i in self.records_data.iter() if
               i.tag.endswith('recordIdentifier') and
               i.text.find(':') > -1]
        return ids

    @property
    def deleted_identifiers(self):
        """
            Return al list of deleted record Identifiers.
        """
        deleted = []
        for item in self.records_data[2]:
            if item.tag.endswith('record'):
                if item[0].tag.endswith('header'):
                    deleted.append(item[0][0].text)
        return deleted


class record():
    """
        Class for parsing XML output from OAI server,
        to more human readable form. This class
        is a generic record level object.

        A record has a bunch of properties, most of them
        are exposed, for example:

        >>> record.alto # Returns the alto files for a record.

        >>> record.image # Returns the image for a record.
                         # Mostly .jpg's
    """
    record_data = False
    DEBUG = False
    current_set = False

    def __init__(self, record_data, current_set=False, debug=False):
        """
            :param record_data: XML object of the wanted record.
            :param debug: enable or disable debuging
        """
        self.record_data = record_data
        self.current_set = current_set

        if debug:
            self.DEBUG = debug

    @property
    def alto(self):
        """
            Return the ALTO(s) for the current record.
            For more information on ALTO see:

            https://en.wikipedia.org/wiki/ALTO_(XML)

            For parsing alto data back to text, use:

            >>> from kb.nl.helpers import alto_to_text
            >>> alto_to_text(alto)
        """
        if self.current_set == "BYVANCK":
            return False

        alto_url_list = []
        alto_url = False

        for item in self.record_data.iter():
            if item.attrib and \
               item.attrib.get('ref') and \
               item.attrib['ref'].lower().endswith(':alto'):

                alto_url = item.attrib['ref']

                if alto_url not in alto_url_list:
                    alto_url_list.append(alto_url)

        if not alto_url:
            for item in self.record_data.iter():
                if item.attrib and \
                   item.attrib.get('ref') and \
                   item.attrib['ref'].lower().endswith('.xml'):

                    alto_url = item.attrib['ref']
                    alto_url_list.append(alto_url)
                    break

        # The result is either one ALTO file,
        # or a bunch of them, if more then one,
        # fetch the results and return a list.
        if len(alto_url_list) <= 1:
            alto_url = alto_url_list[0]

            if self.DEBUG:
                sys.stdout.write(alto_url)

            response = requests.get(alto_url)

            if not response.status_code == 200:
                raise Exception('Error while getting data from %s' % alto_url)

            return [response.text]
        else:
            alto_list = []

            for alto_url in alto_url_list:
                response = requests.get(alto_url)

                if self.DEBUG:
                    sys.stdout.write(alto_url + " ")

                if not response.status_code == 200:
                    raise Exception('Error while getting data from %s' % alto_url)

                alto_list.append(response.text)

            return alto_list

    @property
    def image(self):
        """
            Retrieve the image for the current record,
            and return the bits.
        """
        img_url = False

        if self.current_set == "BYVANCK":
            img_url = 'http://imageviewer.kb.nl/'
            img_url += 'ImagingService/imagingService?id='
            img_url += self.record_data[2][0][1][0][1].text.split('=')[1]
        else:
            for item in self.record_data.iter():
                if item.attrib and \
                   item.attrib.get('ref') and \
                   item.attrib.get('ref').startswith('http://') and \
                   (item.attrib['ref'].endswith(':image') or
                        item.attrib['ref'].endswith('.jpg')):

                    img_url = item.attrib['ref']
                    break

        if not img_url:
            return False

        if self.DEBUG:
            sys.stdout.write(img_url)

        response = requests.get(img_url)

        if not response.status_code == 200:
            raise Exception('Error while getting data from %s' % img_url)

        return response.content

    @property
    def title(self):
        """
            Get corresponding title.
        """
        for item in self.record_data.iter():
            if item.tag.endswith('title'):
                return item.text
        return False

    @property
    def annotation(self):
        """
            Get corresponding annotation.
        """
        for item in self.record_data.iter():
            if item.tag.endswith('annotation'):
                return item.text
        return False

    @property
    def date(self):
        """
            Get timeperiod of creation.
        """
        for item in self.record_data.iter():
            if item.tag.endswith('date'):
                return item.text
        return False

    @property
    def creator(self):
        """
            Get corresponding creator.
        """
        for item in self.record_data.iter():
            if item.tag.endswith('creator'):
                return item.text
        return False

    @property
    def contributor(self):
        """
            Get contributors to this record.
        """
        for item in self.record_data.iter():
            if item.tag.endswith('contributor'):
                return item.text
        return False

    @property
    def publisher(self):
        """
            Get publisher information for this record.
        """
        for item in self.record_data.iter():
            if item.tag.endswith('publisher'):
                return item.text
        return False
