import unittest
import xml.etree.ElementTree as ET

from xsdgen.get_types_from_elem import get_types_from_elem

class TestTypeExtraction(unittest.TestCase):
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
        tree = ET.fromstring(self.sample_xml_0)
        types_dict = get_types_from_elem(tree)
        self.assertNotEqual(len(types_dict["types"]), 0)
        self.assertNotEqual(len(types_dict["root_type"]), 0)

    def test_get_types_from_elem(self):
        tree = ET.fromstring(self.sample_xml_0)
        target_typenames = list(map(lambda ttype: ttype["typename"], self.sample_tree_0["types"]))

        types_dict = get_types_from_elem(tree)
        self.assertEqual(len(types_dict["types"]), len(target_typenames))
        for type_entry in types_dict["types"]:
            typename = type_entry["typename"]
            self.assertIn(typename, target_typenames)
        
        for t in types_dict["types"]:
            if "settings" == t["typename"]:
                self.assertEqual(len(t["attributes"]), 0)
                self.assertEqual(len(t["child_typenames"]), 3)
            if "config" == t["typename"]:
                self.assertEqual(len(t["child_typenames"]), 1)
                self.assertTrue("list:" in t["child_typenames"][0])

        self.assertEqual(types_dict["root_type"], "settings")