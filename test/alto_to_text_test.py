#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('.')
sys.path.append('..' + os.sep)


def alto_to_text_test():
    """
    >>> import os
    >>> import codecs
    >>> from kb.nl.helpers import alto_to_text
    >>> path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    >>> path += "test_data" + os.sep + "anp_1937-10-01_1_alto.xml"
    >>> fh = codecs.open(path, "r", encoding="utf-8")
    >>> data = fh.read()
    >>> fh.close()
    >>> alto_to_text(data).split('\\n')[2][:45]
    ' De Rijksradiocontroledienst heeft te UTRECHT'
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
