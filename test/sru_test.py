#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('..' + os.sep)
sys.path.append('.' + os.sep)

def oai_anp():
    """
    >>> from kb.nl.api import sru
    >>> from kb.nl.helpers import alto_to_text

    >>> sru.DEBUG=True
    >>> response = sru.search("beatrix", "ANP")
    http://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=50&operation=searchRetrieve&startRecord=1&recordSchema=dcx&x-collection=ANP&query=beatrix
    >>> response.nr_of_records
    5638
    >>> response.nr_of_retrieved_records
    50
    >>> records = response.records
    >>> [r.date for r in records][:3]
    ['1980/05/21 00:00:00', '1962/11/09 00:00:00', '1977/03/17 00:00:00']
    >>> response = sru.search("juliana", "ANP")
    http://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=50&operation=searchRetrieve&startRecord=1&recordSchema=dcx&x-collection=ANP&query=juliana
    >>> response.nr_of_records
    6445
    >>> records = response.records
    >>> [r.date for r in records][:3]
    ['1948/08/28 00:00:00', '1950/09/16 00:00:00', '1949/09/23 00:00:00']
    >>> records[1].title
    'ANP Nieuwsbericht - 16-09-1950 - 42'
    >>> records[1].abstract.strip()[:10]
    u'Bik 16 Sep'
    >>> len(records)
    50
    >>> response = []
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
