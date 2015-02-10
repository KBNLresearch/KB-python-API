#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from kb.nl.api import sru
from kb.nl.api import oai
from kb.nl.helpers import alto_to_text

oai_handler = oai
oai_handler.current_set = "ANP"

response = sru.search("beatrix AND juliana AND Bernhard AND telegram", "ANP")
print "Number of records: %i" % response.sru.nr_of_records

record_nr = 0

for record in response.records:
    record_nr += 1
    print("********~ Record number %i ~*********" % record_nr)
    print("Date: %s" % record.date)
    print("RecordIdentifier: %s" % record.identifier)
    print("Abstract: %s" % record.abstract)
    print("Title: %s" % record.title)

    record = oai_handler.get(record.identifier)

    for alto in record.alto:
        print("Fulltext: %s" % alto_to_text(alto))

    print("*************************************\n\n")
