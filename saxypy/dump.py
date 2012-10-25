"""
This module provides ways of dumping Python data structures into XML.
"""

from saxypy.utils import PeekGenerator, escape_for_xml


EVENT_ATTRIBUTE = 1
EVENT_NODE = 2
EVENT_CDATA = 3


class DataEventGenerator(object):
    """
    Take a Python data structure and generate events that will later
    be used to build an XML output.
    """

    def __call__(self, data):
        """
        Invokable object--set up a new name stack and recursively
        generate XML events.
        """
        self._name_stack = []
        return self._make_events(data)

    def _make_events(self, data):
        """
        Recursively walk the given data structure and generate XML
        events.
        """
        if dict in type(data).__bases__:
            for key in data:
                if key[0] == '@':
                    yield EVENT_ATTRIBUTE, key[1:], data[key]
            for key in data:
                if key[0] == '@':
                    continue

                self._name_stack.append(key)
                if type(data[key]) not in (list, tuple):
                    yield EVENT_NODE, key

                for result in self._make_events(data[key]):
                    yield result

                self._name_stack.pop()
                if type(data[key]) not in (list, tuple):
                    yield -EVENT_NODE, key
        elif type(data) in (list, tuple):
            for element in data:
                yield EVENT_NODE, self._name_stack[-1]

                for result in self._make_events(element):
                    yield result

                yield -EVENT_NODE, self._name_stack[-1]
        else:
            yield EVENT_CDATA, str(data)


def xml_struct_stream_transformer(event_gen):
    """
    Turn raw events from DataEventGenerator into something a bit more
    structured and more client-friendly.
    """
    gen = PeekGenerator(event_gen)
    current_depth = 0
    for event in gen:
        if event[0] == EVENT_NODE:
            attributes = []
            text = None
            while gen.has_next():
                sub_event = gen.peek()
                if sub_event[0] == EVENT_ATTRIBUTE:
                    attributes.append(sub_event[1:])
                    gen.next()
                elif sub_event[0] == EVENT_CDATA:
                    text = sub_event[1]
                    gen.next()
                else:
                    break
            yield current_depth, event[1], attributes, text
            current_depth += 1
        elif event[0] == -EVENT_NODE:
            current_depth -= 1
            yield current_depth, event[1]
        else:
            raise ValueError('unknown event code: %s (%s)' % (
                event[0], type(event[0])))


def gen_to_xml_stream(gen, **kwargs):
    """
    Given a generator from xml_struct_stream_transformer, create a
    stream of text tokens representing the given XML document generated.
    """
    indent = kwargs.get('indent', '    ')
    line_sep = kwargs.get('line_sep', '\n')

    for event in gen:
        next_event = gen.peek()
        if len(event) == 4:
            attributes = []
            for key, value in event[2]:
                attributes.append('%s="%s"' % (key, escape_for_xml(value)))
            attributes_str = ' '.join(attributes)

            yield indent * event[0]
            if len(next_event) == 2:
                if not event[3]:
                    if len(attributes):
                        yield '<%s %s/>' % (event[1], ' '.join(attributes))
                    else:
                        yield '<%s/>' % event[1]
                else:
                    if len(attributes):
                        yield '<%s %s>%s</%s>' % (
                            event[1], ' '.join(attributes), event[3], event[1])
                    else:
                        yield '<%s>%s</%s>' % (event[1], event[3], event[1])
                yield line_sep
                gen.next()
            else:
                if len(attributes):
                    yield '<%s %s>' % (event[1], ' '.join(attributes))
                else:
                    yield '<%s>' % event[1]
                yield line_sep
                if event[3]:
                    yield indent * (event[0] + 1)
                    yield event[3]
                    yield line_sep
        else:
            yield indent * event[0]
            yield '</%s>' % event[1]
            yield line_sep


def struct_to_xml_stream(data, **kwargs):
    """
    User-friendly wrapper of the algorithms defined in this module to
    turn a Python data structure into a stream of text tokens
    representing an XML document.
    """
    event_gen = DataEventGenerator()(data)
    data_gen = PeekGenerator(xml_struct_stream_transformer(event_gen))
    return gen_to_xml_stream(data_gen, **kwargs)
