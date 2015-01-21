#!/usr/bin/env python

import os
import sys

sys.path.append('..' + os.sep)
sys.path.append('.' + os.sep)

def oai_anp():
    """
    >>> from kb.nl.api import oai
    >>> from kb.nl.helpers import alto_to_text
    >>> oai.DEBUG=True
    >>> oai.list_sets()
    ['ANP', 'BYVANCK', 'DPO', 'SGD']
    >>> records = oai.list_records("ANP")
    http://services.kb.nl/mdo/oai?verb=ListRecords&metadataPrefix=didl&set=anp
    >>> records.identifiers[:3]
    ['anp:1937:10:01:1', 'anp:1937:10:01:2', 'anp:1937:10:01:3']
    >>> len(oai.resumptiontoken)
    42
    >>> record = oai.get(records.identifiers[0])
    http://services.kb.nl/mdo/oai?verb=GetRecord&identifier=anp:anp:1937:10:01:1:mpeg21&metadataPrefix=didl
    >>> alto_records = record.alto
    http://resolver.kb.nl/resolve?urn=anp:1937:10:01:1:mpeg21:alto
    >>> len(alto_records[0])
    90124
    >>> alto_to_text(alto_records[0]).split("\\n")[1][:27]
    u' RADIO 1 van 1 Ootober 1937'
    >>> image_record = record.image
    http://resolver.kb.nl/resolve?urn=anp:1937:10:01:1:mpeg21:image
    >>> len(image_record)
    721035
    >>> record.title
    'ANP Nieuwsbericht - 01-10-1937 - 1'
    >>> record.date
    '1937-10-01'
    """


def oai_sgd():
    """
    >>> from kb.nl.api import oai
    >>> oai.DEBUG=True
    >>> records = oai.list_records("SGD")
    http://services.kb.nl/mdo/oai?verb=ListRecords&metadataPrefix=dcx&set=sgd:register
    >>> records.identifiers[:1]
    ['sgd:register:mpeg21:1967:0001424:L0000:lemma']
    >>> len(oai.resumptiontoken)
    50
    >>> record = oai.get(records.identifiers[0])
    http://services.kb.nl/mdo/oai?verb=GetRecord&identifier=SGD:sgd:mpeg21:1967:0001424&metadataPrefix=didl
    >>> alto_records = record.alto # SGD does not have real alto files..
    http://resourcessgd.kb.nl/SGD/1967/FULLTEXT/SGD_1967_tekst_0003969.xml
    >>> len(alto_records[0])
    4777
    """


def oai_dpo():
    """
    >>> from kb.nl.api import oai
    >>> from kb.nl.helpers import alto_to_text
    >>> oai.DEBUG=True
    >>> records = oai.list_records("DPO")
    http://services.kb.nl/mdo/oai?verb=ListRecords&metadataPrefix=didl&set=DPO
    >>> records.identifiers[:3]
    ['dpo:10221:mpeg21', 'dpo:10863:mpeg21', 'dpo:10864:mpeg21']
    >>> len(oai.resumptiontoken)
    42
    >>> records = oai.list_records("DPO") # doctest: +ELLIPSIS
    http://services.kb.nl/mdo/oai?verb=ListRecords&metadataPrefix=didl&set=DPO&resumptionToken...
    >>> records.identifiers[:3]
    ['dpo:10007:mpeg21', 'dpo:10008:mpeg21', 'dpo:10009:mpeg21']
    >>> record = oai.get(records.identifiers[0])
    http://services.kb.nl/mdo/oai?verb=GetRecord&identifier=DPO:dpo:10007:mpeg21&metadataPrefix=didl
    >>> alto_records = record.alto # doctest: +ELLIPSIS
    http://resolver.kb.nl/resolve?urn=dpo:10007:mpeg21:0001:alto http://...
    >>> len(alto_records[0])
    21634
    >>> record.title[:20]
    'Aanmerkingen, wegens'
    >>> record.contributor
    False
    >>> record.publisher
    False
    """


def oai_byvanck():
    """
    >>> from kb.nl.api import oai
    >>> oai.DEBUG=True
    >>> records = oai.list_records("BYVANCK")
    http://services.kb.nl/mdo/oai?verb=ListRecords&metadataPrefix=dcx&set=BYVANCK
    >>> records.deleted_identifiers[:2]
    ['BYVANCK:BYVANCK:3477', 'BYVANCK:BYVANCK:5562']
    >>> records.identifiers
    ['BYVANCK:3477']
    >>> record = oai.get(records.identifiers[0])
    http://services.kb.nl/mdo/oai?verb=GetRecord&identifier=ByvanckB:ByvanckB:3477&metadataPrefix=dcx
    >>> record.alto
    False
    >>> image = record.image
    http://imageviewer.kb.nl/ImagingService/imagingService?id=BYVANCKB:mimi_78d38:dl1_183r_min
    >>> len(image)
    109258
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
