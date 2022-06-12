import xml.etree.ElementTree as ET
from xsdgen.get_types_from_elem import _ContentType

def _handle_empty(type_info, root):
    type_def = ET.SubElement(root, "xs:complexType", {"name" : f"{type_info.type_name}Type"})
    for attrib_name in type_info.attributes:
        attribs = 
        {
            "name" : attrib_name,
            "type" : "xs:string",
            "use" : "required"
        }
        attrib_elem = ET.SubElement(type_def, "xs:attribute", attribs)

def _handle_text(type_info, root):
    type_def = ET.SubElement(root, "xs:complexType", {"name" : f"{type_info.type_name}Type"})
    content_t = ET.SubElement(type_def, "xs:simpleContent")
    ext_t = ET.SubElement(content_t, "xs:extension", {"base" : "xs:string"})
    for attrib_name in type_info.attributes:
        attribs = 
        {
            "name" : attrib_name,
            "type" : "xs:string",
            "use" : "required"
        }
        attrib_elem = ET.SubElement(ext_t, "xs:attribute", attribs)

def _handle_types(type_info, root):
    type_def = ET.SubElement(root, "xs:complexType", {"name" : f"{type_info.type_name}Type"})
    seq_t = ET.SubElement(type_def, "xs:sequence")
    # TODO what about the attributes of this type?
    for child_type_name in type_info.child_type_names:
        attribs = 
        {
            "name" : child_type_name,
            "type" : f"{child_type_name}Type",
            "minOccurs" : 1,
            "maxOccurs" : "unbounded"
        }
        attrib_elem = ET.SubElement(seq_t, "xs:element", attribs)

def _handle_mixed(type_info, root):
    raise NotImplementedError("Handling mixed content (elems and text) not implemented yet")

def get_xsd_from_types(types):
    """converts types to xsd as string

    Args:
        types : dict containing the types to define 
                and the root element type

    Returns:
        xsd as element tree
    """
    ns = {"xmlns:xs" : "http://www.w3.org/2001/XMLSchema"}
    ET.register_namespace('xs', "http://www.w3.org/2001/XMLSchema")
    root = ET.Element("xs:schema", {"xmlns:xs" : "http://www.w3.org/2001/XMLSchema"})
    case_content_type = 
    {
        _ContentType.empty : _handle_empty,
        _ContentType.text : _handle_text,
        _ContentType.types : _handle_types,
        _ContentType.mixed : _handle_mixed
    }
    for type_info in types["types"]:
        case_content_type[type_info.content_type](type_info, root)
    # for namespace population convert it to string and then back to element
    return ET.fromstring(ET.tostring(root))