"""
Defines the handler class an a convenience function for parsing XML
using the SAX libraries.
"""

import xml.sax
from saxypy.dump import struct_to_xml_stream


def dump(data, **kwargs):
    """
    Convenience function to turn a Python data structure into an XML
    document.
    """
    return ''.join(struct_to_xml_stream(data, **kwargs))


def parse(thing, **kwargs):
    """
    Understands how to parse strings or file-like objects.

    Optional keyword arguments:
        strip_whitespace = True|False (default True)
    """
    handler = SaxyHandler(**kwargs)
    if isinstance(thing, basestring):
        xml.sax.parseString(thing, handler)
    else:
        xml.sax.parse(thing, handler)
    return handler.data


class SaxyHandler(xml.sax.ContentHandler):
    """
    The handler class used by SAX parser events to incrementally build
    the XML document.
    """

    def __init__(self, **kwargs):
        """
        Set up handler configuration.
        """
        xml.sax.ContentHandler.__init__(self)
        self.strip_whitespace = kwargs.get('strip_whitespace', True)
        self.data = None
        self.parents = None

    def startDocument(self):
        """
        Create new data structures for keeping track of the document
        and recursion depth at the start of each document.

        Doing it at the start of each document allows a single handler
        instance to be used for parsing multiple XML files.
        """
        self.data = {}
        self.parents = []

    def endDocument(self):
        """
        Called at the end of a document.
        """

    def startElement(self, name, attrs):
        """
        Called whenever a new element is encountered. There is a bit of
        logic to make sure that things are nested in a way that makes
        sense.
        """
        sub_struct = {}
        if name in self.data:
            if type(self.data[name]) == list:
                self.data[name].append(sub_struct)
            else:
                self.data[name] = [self.data[name], sub_struct]
        else:
            self.data[name] = sub_struct
        self.parents.append(self.data)
        self.data = sub_struct
        for qname in attrs.getQNames():
            sub_struct['@' + qname] = attrs.getValueByQName(qname)

    def endElement(self, name):
        """
        Called whenever an element ends (usually the closing tag). There
        is some logic here to make sure that things in the child data
        structure are not nested when they do not need to be.
        """
        self.data = self.parents.pop()
        if not len(self.data[name]):
            self.data[name] = None
        elif len(self.data[name]) == 1:
            self.data[name] = self.data[name].values()[0]

    def characters(self, content):
        """
        Called by the SAX parser whenever data is encountered between
        tags.
        """
        if self.strip_whitespace:
            content = content.strip()
        if content:
            self.data['*content*'] = content
