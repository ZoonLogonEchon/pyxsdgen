class _TypeHierarchy(object):
    """
    docstring
    """
    def __init__(self):
        self.type_hierarchy = {"types" : []}

    def find_type(self, elem):
        """Searches for elem in the type hierarchy

        Args:
            elem: ElementTree Element

        Returns:
            type entry if found else None
        """
        for t in self.type_hierarchy["types"]:
            if elem.tag in t["typename"]:
                return t
        else:
            return None

    def build_hierachy(self, elem):
        """Builds the type hierarchy recursively

        Fills the type hierarchy. Multiple calls of this function
        on the same object lead to undefined state of the hierarchy

        Args:
            elem: ElementTree Element

        Returns:
            final call returns the type of the root element
        """
        t = self.find_type(elem)
        if t:
            return t
        if not len(elem):
            # leaf node 
            test = {
                "typename" : elem.tag,
                "attribute" : [k for k in elem.attrib.keys()],
                "child_typenames" : []
            }
            self.type_hierarchy["types"].append(test)
            return test
        else:
            # subtree node
            child_typenames = [] 
            for child in elem:
                t = self.build_hierachy(child)
                formatted_tname = ":" + t["typename"]
                child_typenames.append(formatted_tname)
            ctns = list(child_typenames)
            seq_dict = {}
            for i, c in enumerate(ctns):
                if (i + 1) == len(ctns):
                    break
                _, cbasetype = c.split(":")
                _, nbasetype = ctns[i + 1].split(":")
                if cbasetype == nbasetype:
                    if not cbasetype in seq_dict:
                        seq_dict.update({cbasetype : [i, i + 1] })
                    else:
                        seq_dict[cbasetype][1] = i + 1
            for seq_type, index_range in seq_dict.items():
                del child_typenames[index_range[0] : index_range[1] + 1]
                child_typenames.insert(index_range[0], "list:{}".format(seq_type))
            test = {
                "typename" : elem.tag,
                "attribute" : [k for k in elem.attrib.keys()],
                "child_typenames" : child_typenames
            }
            self.type_hierarchy["types"].append(test)
            return test

def get_types_from_elem(elem):
    """extracts simple and complex type from xml element

    Args:
        elem: ElementTree Element
    
    Returns:
        dictionary with keys "types" and "root_type".
        "types" is a list of dicts {typename : str, typeattrs : List[str], children : List[str]}
        "root_type" is the typename of the root of elem
    """
    root_typename = elem.tag
    r = _TypeHierarchy()
    r.build_hierachy(elem)
    return { "types" : r.type_hierarchy["types"], "root_type" : root_typename}