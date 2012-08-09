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
