SaxyPy
======

Dealing with XML is a chore, no matter what language.  It should be as easy
as JSON, but for some reason it isn't.  Wasn't.  It is now:

```python
import json
import saxypy

data = saxypy.parse(open('example.xml', 'r'))
print json.dumps(data, sort_keys=True, indent=4)
```

```python
import saxypy

data = {
    'root': {
        'item': [
            {
                '@id': 1,
                'name': 'something',
            },
            {
                '@id': 2,
                'name': 'other thing',
            },
        ],
    },
}
print saxypy.dump(data)
```

That's it.  As it should have always been.
