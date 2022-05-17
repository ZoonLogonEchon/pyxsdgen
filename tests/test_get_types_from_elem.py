import unittest
import xml.etree.ElementTree as ET

from xsdgen.get_types_from_elem import get_types_from_elem

class TestTypeExtraction(unittest.TestCase):
    """
    docstring
    """
    sample_xml_0 ="""<?xml version="1.0"?>
        <settings>
            <projectauthor name="Daimo Nia" />
            <projectpath base="path_base">rel path</projectpath>
            <config>
                <attributeA> 123 </attributeA>
                <attributeB> abc </attributeB>
            </config>
        </settings>
        """
    def test_not_empty(self):
        tree = ET.fromstring(self.sample_xml_0)
        types_dict = get_types_from_elem(tree)
        self.assertNotEqual(len(types_dict["types"]), 0)
        self.assertNotEqual(len(types_dict["root_type"]), 0)

    def test_get_types_from_elem(self):
        tree = ET.fromstring(self.sample_xml_0)
        target_typenames = ["attributeA", "attributeB", "config", "settings", "projectauthor", "projectpath"]

        types_dict = get_types_from_elem(tree)

        self.assertEqual(len(types_dict["types"]), len(target_typenames))
        for type_entry in types_dict["types"]:
            typename = type_entry["typename"]
            self.assertIn(typename, target_typenames)
        
        self.assertEqual(types_dict["root_type"], "settings")