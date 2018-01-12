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
    >>> response = sru.search("beatrix AND juliana AND Bernhard AND gelukwensen", "ANP")
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=1&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    >>> for record in response.records:
    ...     print(record.dates)
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=1&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    ['1967/04/28 00:00:00']
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=2&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    ['1968/09/25 00:00:00']
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=3&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    ['1966/02/21 00:00:00']
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=4&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    ['1966/03/10 00:00:00']
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=5&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    ['1966/03/09 00:00:00']
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=6&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    ['1969/10/11 00:00:00']
    run_query: https://jsru.kb.nl/sru/sru?version=1.2&maximumRecords=1&operation=searchRetrieve&startRecord=7&recordSchema=dcx&x-collection=ANP&query=beatrix%20AND%20juliana%20AND%20Bernhard%20AND%20gelukwensen
    ['1965/06/29 00:00:00']
    >>> sru.DEBUG = False
    >>> response = sru.search('"J.A. Deelder" AND "gevallen"', "GGC")
    >>> for i, record in enumerate(sorted(response.records)):
    ...     print(record.titles, record.dates)
    ...     break
    (['Zij die vielen zijn gevallen / J.A. Deelder ; [foto: Pieter van Oudheusden]'], ['[ca. 1990]'])
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
