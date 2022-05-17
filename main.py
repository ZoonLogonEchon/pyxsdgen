import argparse

def main(args):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate xsd file from xml file')
    parser.add_argument('path_to_xml', type=str,
                    help='path to the xml file')
    args = parser.parse_args()
    main(args)