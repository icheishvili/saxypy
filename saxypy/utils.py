"""
Various utilities used by saxypy. Things that do not belong anywhere
else go in here.
"""


def pretty_format(obj):
    """
    Pretty print a given object. Use JSON if it's available, otherwise
    fall back to Python's native pretty printer.
    """
    try:
        import json
        return json.dumps(obj, sort_keys=True, indent=4)
    except ImportError:
        from pprint import pformat
        return pformat(obj)


class PeekGenerator(object):
    """
    Allows the user to look one object ahead in a generator stream.
    """

    def __init__(self, gen):
        """
        Set up the object with the generator to wrap.
        """
        self.gen = gen
        self.buffer = None

    def __iter__(self):
        """
        Expose this class to Python as something that can be iterated on.
        """
        return self

    def has_next(self):
        """
        Check to see if the generator has any more items. This has the
        side-effect of possibly getting the next item from the
        underlying generator.
        """
        if self.buffer:
            return True
        try:
            self.buffer = self.gen.next()
            return True
        except StopIteration:
            return False

    def next(self):
        """
        Get the next item if there is one, otherwise raise a
        StopIteration exception.
        """
        if not self.has_next():
            raise StopIteration()

        if self.buffer:
            value = self.buffer
            self.buffer = None
            return value
        else:
            return self.gen.next()

    def peek(self):
        """
        Look at the next object in the generator stream, but do not
        consume it.
        """
        if not self.buffer:
            self.has_next() # side-effect
        return self.buffer


def escape_for_xml(value):
    """
    Escape give value so that it can be safely used in an XML document.
    """
    value = str(value)
    table = [
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ("'", '&apos'),
        ('"', '&quot;')
    ]
    for search_for, replace_with in table:
        value = value.replace(search_for, replace_with)
    return value
