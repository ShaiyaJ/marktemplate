from xml.dom import minidom
import sys
import glob

def process_node(target: minidom.Node):
    """Processes a single node"""

    if target.nodeType == minidom.Node.ELEMENT_NODE:
        match (target.tagName): # TODO: make includes search for closest src
                                    # TODO: make .closest and refactor code
                                    # TODO: make process_children and refactor code
            case "mt-raw-include":
                src = target.getAttribute("src")
                target.parentNode.replaceChild(minidom.parse(src).documentElement, target)
                
                
            case "mt-text-include":
                src = target.getAttribute("src")
                
                with open(src, "r") as file:
                    value = file.read()
                    file.close()
                    
                target.parentNode.replaceChild(minidom.Document().createTextNode(value), target)
                    
                    
            case "mt-include":
                src = target.getAttribute("src")

                root = minidom.parse(src).documentElement
                
                target.appendChild(root)                        # Append as child so <mt-attr> works when the attribute is on the mt-include tag
                process_node(root)
                
                target.parentNode.replaceChild(root, target)    # Replace the target with root - effectively deleting target and moving it's child up
                return                                          # Root node has already been processed, so we don't need to run the final for loop
                        
                            
            case "mt-glob":
                src = target.getAttribute("src")
                
                files = glob.glob(src)
                
                for file in files:
                    clone = target.cloneNode(True)
                    
                    for child in clone.childNodes:
                        if child.nodeType != minidom.Node.ELEMENT_NODE:
                            continue
                    
                        child.setAttribute("src", file)
                        node = target.parentNode.insertBefore(child, target)
                    
                        process_node(node)
                        
                target.parentNode.removeChild(target)
                return


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
    
