from xml.dom import minidom
import sys


def process_node(target: minidom.Node) -> minidom.Node:
    """Processes a single node"""

    if target.nodeType == minidom.Node.ELEMENT_NODE:
        match (target.tagName):
            case "mt-raw-include":
                src = target.getAttribute("src")
                target.parentNode.replaceChild(minidom.parse(src).documentElement, target)
                    
                    
            case "mt-include":
                src = target.getAttribute("src")

                root = minidom.parse(src).documentElement
                target.parentNode.replaceChild(root, target)
                process_node(root)
                    

            case "mt-attr":
                attr = target.getAttribute("name")
                parent = target
                    
                while (parent.getAttribute(attr) == ""):
                    parent = parent.parentNode
                        
                value = parent.getAttribute(attr)
                target.parentNode.replaceChild(minidom.Document().createTextNode(value), target)


    for child in target.childNodes:
        process_node(child)



def processFile(path: str, encoding: str = "utf8") -> str:
    """Processes a single marktemplate file into a static html file"""

    # Process root node
    doc = minidom.parse(path)
    process_node(doc.documentElement)

    # Stringify and return
    return doc.documentElement.toxml()


# Main
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: no target file provided", file=sys.stderr);
        sys.exit(1);
        
    target = sys.argv[1];

    # Process file
    print(processFile(target))
    
