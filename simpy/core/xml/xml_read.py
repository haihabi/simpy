import xml.etree.ElementTree as et
from .__xml_class__ import XMLTree


def read_xml(xml_file_path):
    return XMLTree(et.parse(xml_file_path).getroot())
