#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from kb.nl.api import sru
from kb.nl.api import oai
from kb.nl.helpers import alto_to_text

oai_handler = oai
oai_handler.current_set = "ANP"

response = sru.search("karel AND reve AND hooftprijs", "ANP")
print ("Number of records: %i" % response.sru.nr_of_records)

record_nr = 0

for record in response.records:
    record_nr += 1
    print("********~ Record number %i ~*********" % record_nr)
    print("Date: %s" % record.dates)
    print("RecordIdentifier: %s" % record.identifiers)
    print("Abstract: %s" % record.abstracts)
    print("Title: %s" % record.titles)
    oai_handler.DEBUG = True
    r = oai_handler.get(record.identifiers[0])
    for alto in r.alto:
        print("Fulltext: %s" % alto_to_text(alto))
