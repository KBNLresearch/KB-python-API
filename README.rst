.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Logo_Koninklijke_Bibliotheek_wordmark.svg/120px-Logo_Koninklijke_Bibliotheek_wordmark.svg.png
        :alt: Koninklijke Bibliotheek Logo
        :align: right
        :scale: 50 %
        :width: 100 px
        :height: 100 px
 

.. _API: https://en.wikipedia.org/wiki/Application_programming_interface
.. _DataServices: http://www.kb.nl/bronnen-zoekwijzers/dataservices-en-apis
.. _Delpher: http://www.delpher.nl/
.. _KB: http://www.kb.nl/en
.. _OAI-MPH: http://www.openarchives.org/pmh/
.. _Python: http://python.org/
.. _SRU: http://www.loc.gov/standards/sru/
.. _Travis: https://travis-ci.org/KBNLresearch/KB-python-API
.. _CC-BY-NC-ND: https://creativecommons.org/licenses/by-nc-nd/2.0/
.. _pypi: https://pypi.python.org/pypi/kb/

=====================================================================
KB python API: Access to National Library of the Netherlands datasets
=====================================================================

.. image:: https://api.travis-ci.org/KBNLresearch/KB-python-API.svg
        :alt: build status
        :align: left
Travis_ build status


KB-Python-API is a simple API_ for Python_, the API provides easy access to free and CC-BY-NC-ND_ datasets provided by the National Library of the Netherlands (KB_).

It relies on the back-end infrastructure of the KB_ which consists of an SRU_ and OAI-MPH_ service. The KB Python API makes it easy to interact with historical data,
for more information on the provided datasets and data-rights take a look at the DataServices_ page of the KB.

For example usage have a look at the provided example.py file, or consult the /test directory.

This package is also available from the pypi_ website.
To do a quick install:

.. code-block:: python
pip install kb


OAI example
===========
.. code-block:: python

    >>> from kb.nl.api import oai
    >>> from kb.nl.helpers import alto_to_text
    >>> oai.list_sets()
    ['ANP', 'BYVANCK', 'DPO', 'SGD']
    >>> records = oai.list_records("ANP")
    >>> records.identifiers[:3]
    ['anp:1937:10:01:1', 'anp:1937:10:01:2', 'anp:1937:10:01:3']
    >>> len(oai.resumptiontoken)
    42
    >>> record = oai.get(records.identifiers[0])
    >>> alto_record = record.alto
    >>> alto_to_text(alto_record[0]).split("\\n")[1][:27]
    u' RADIO 1 van 1 Ootober 1937'
    >> image_record = record.image
    >>> len(image_record)
    721035

SRU example
===========
.. code-block:: python

    >>> from kb.nl.api import sru
    >>> from kb.nl.helpers import alto_to_text
    >>> response = sru.search("Beatrix AND Juliana AND Bernhard AND telegram", "ANP")
    >>> for record in response.records:
    ...     print("Date: %s" % record.date)
    ...     print("Abstract: %s" % record.abstract) 
    ...     print("Title: %s" % record.title)
