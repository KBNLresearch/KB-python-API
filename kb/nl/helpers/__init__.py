try:
    from lxml import etree
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                except ImportError:
                    raise("Failed to import ElementTree from any known place")


def alto_to_text(alto_data):
    ''' Grab the selected text blocks and write them to disk '''
    alto_data = etree.fromstring(alto_data.encode('utf-8'))

    alto_text = u""
    prev_was_hyp = False

    for item in alto_data.iter():
        if item.tag.endswith("String"):
            if prev_was_hyp:
                alto_text += item.get("CONTENT")
                prev_was_hyp = False
            else:
                alto_text += u" " + item.get("CONTENT")

        if item.tag.endswith("HYP"):
            prev_was_hyp = True

        if item.tag.endswith("TextBlock"):
            if len(alto_text) > 0:
                alto_text += u"\n"

    return alto_text
