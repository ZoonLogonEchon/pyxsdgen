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
        """Builds the type hierarchy

        Fills the type hierarchy. Multiple calls of this function
        on the same object lead to undefined state of the hierarchy

        Args:
            elem: ElementTree Element

        Returns:
            type of root element
        """
        t = self.find_type(elem)
        if t:
            return t
        if not len(elem):
            # leaf node 
            test = {
                "typename" : elem.tag
            }
            self.type_hierarchy["types"].append(test)
            return test
        else:
            # subtree node
            child_typenames = [] 
            for child in elem:
                t = self.build_hierachy(child)
                child_typenames.append(t["typename"])
            test = {
                "typename" : elem.tag,
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