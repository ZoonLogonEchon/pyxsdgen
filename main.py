import argparse
import xml.etree.ElementTree as ET
import xmlschema

def main(args):
    tree = ET.parse(args.path_to_xml)
    root = tree.getroot()
    print(ET.tostring(root).decode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate xsd file from xml file')
    parser.add_argument('path_to_xml', type=str,
                    help='path to the xml file')
    args = parser.parse_args()
    my_schema = xmlschema.XMLSchema('sample.xsd')
    my_schema.validate("sample.xml")
    #main(args)