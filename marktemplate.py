from xml.dom import minidom
import sys
import glob


def closest(node, attr):
    """Finds the closest parent that has an attribute"""

    current_attr = node.getAttribute(attr)       
    
    if current_attr != "":
        return current_attr

    return closest(node.parentNode, attr)



def process_node(target: minidom.Node) -> minidom.Node:
    if target.nodeType == minidom.Node.ELEMENT_NODE:
        match target.tagName:
            case "mt-attr":
                name = target.getAttribute("name")
                value = closest(target, name)

                return minidom.Document().createTextNode(value)

            case "mt-for":
                pass
            case "mt-glob":
                pass
            case "mt-include":
                pass
            case "mt-raw-include":
                pass
            case "mt-text-include":
                pass

    # Create clone node 
    clone = target.cloneNode(False)

    for child in target.childNodes:
        clone.appendChild(process_node(child))

    return clone


def processFile(path: str, encoding: str = "utf8") -> str:
    """Processes a single marktemplate file into a static html string"""

    # Process root node
    src = minidom.parse(path)
    return process_node(src.documentElement).toxml()


def processRaw(raw: str) -> str:
    """Processes a parsed raw string into a static html string"""

    # Process root node
    src = minidom.parseString(raw)
    return process_node(src.documentElement).toxml()


# Main
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: no target file provided", file=sys.stderr);
        sys.exit(1);
        
    target = sys.argv[1];

    # Process file
    print(processFile(target))
    
