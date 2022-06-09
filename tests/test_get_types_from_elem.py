import unittest
import xml.etree.ElementTree as ET

from xsdgen.get_types_from_elem import get_types_from_elem
from xsdgen.get_types_from_elem import ElemTypeInfo, _ContentType

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
                ElemTypeInfo("projectauthor", _ContentType.empty, ["name", "homepage"]),
                ElemTypeInfo("projectpath", _ContentType.text, ["base"]),
                ElemTypeInfo("attribute", _ContentType.text, ["name"]),
                ElemTypeInfo("config", _ContentType.types, [], [("list", "attribute")]),
                ElemTypeInfo("settings", _ContentType.types, [], [("element", "projectauthor"), ("element", "projectpath"), ("element", "config")])
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

        types_dict = get_types_from_elem(tree)
        self.assertEqual(len(types_dict["types"]), len(self.sample_tree_0["types"]))
        
        for i in range(len(self.sample_tree_0["types"])):
            self.assertEqual(types_dict["types"][i].content_type, self.sample_tree_0["types"][i].content_type)
            self.assertEqual(types_dict["types"][i].attributes, self.sample_tree_0["types"][i].attributes)
            self.assertEqual(types_dict["types"][i].child_type_names, self.sample_tree_0["types"][i].child_type_names)
            self.assertEqual(types_dict["types"][i].type_name, self.sample_tree_0["types"][i].type_name)

        self.assertEqual(types_dict["root_type"], self.sample_tree_0["root_type"])