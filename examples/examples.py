import saxypy
import saxypy.utils

handle = open('music-example.xml', 'r')
data = saxypy.parse(handle)
print saxypy.utils.pretty_format(data)
handle.close()

handle = open('with-namespaces.xml', 'r')
xml_string = handle.read()
handle.close()
data = saxypy.parse(xml_string)
print saxypy.utils.pretty_format(data)