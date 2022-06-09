import unittest
import xml.etree.ElementTree as ET

from xsdgen.get_xsd_from_types import get_xsd_from_types

class TestXSDStrGeneration(unittest.TestCase):
    """
    docstring
    """
    sample_xml_0 ="""<?xml version="1.0"?>
        <settings>
            <projectauthor name="Daimo Nia" homepage="127.0.0.1" />
            <projectpath base="path_base">rel path</projectpath>
            <config>
                <attribute name="a"> 123 </attribute>
                <attribute name="b"> abc </attribute>
            </config>
        </settings>
        """
    sample_xml_0 ="""<?xml version="1.0"?>
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        
            <settings>
                <projectauthor name="Daimo Nia" homepage="127.0.0.1" />
                <projectpath base="path_base">rel path</projectpath>
                <config>
                    <attribute name="a"> 123 </attribute>
                    <attribute name="b"> abc </attribute>
                </config>
            </settings>
        </xs:schema>
        """
    sample_tree_0 ={
        "types" : [
                {"typename":"attribute", "attributes": ["name"]},
                {"typename":"config", "attributes": [], "child_typenames" : ["list:attribute"]},
                {"typename":"projectauthor", "attributes": []},
                {"typename":"projectpath", "attributes": []},
                {"typename":"settings", "attributes": [], "child_typenames" : [":projectauthor", ":projectpath", ":config"]}
            ],
        "root_type" : "settings"
    }
    def test_not_empty(self):
        xsd_str = get_xsd_from_types(self.sample_xml_0)
        self.assertNotEqual(len(xsd_str), 0)

    def test_get_xsd_from_types(self):
        xsd_str = get_xsd_from_types(self.sample_xml_0)
        pass

    def test_validate_sample_xml(self):
        tree = ET.fromstring(self.sample_xml_0)
        xsd_str = get_xsd_from_types(self.sample_xml_0)
        pass