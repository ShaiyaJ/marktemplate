from xml.dom import minidom
import sys
import glob


def closest(node, attr):
    """Finds the closest parent that has an attribute"""

    current = node

    while True:
        current_attr = current.getAttribute(attr)       
        
        if attr != "":
            return current_attr

        # If the attribute is empty set current to parent
        current = current.parentNode



def process_node(target: minidom.Node):
    """Processes a single node"""

    # If it's an element node then it is possible that it is one of the mt-* elements
    if target.nodeType == minidom.Node.ELEMENT_NODE:
        match target.tagName:
            case "mt-raw-include":                              # Including raw file contents
                src = closest(target, "src")
                target.parentNode.replaceChild(minidom.parse(src).documentElement, target)
                
                
            case "mt-text-include":                             # Including raw file contents as text
                src = closest(target, "src")
                
                with open(src, "r") as file:
                    value = file.read()
                    file.close()
                    
                target.parentNode.replaceChild(minidom.Document().createTextNode(value), target)
                    
                    
            case "mt-include":                                  # Including file contents - processing it as apart of the DOM
                src = closest(target, "src")

                root = minidom.parse(src).documentElement
                
                target.appendChild(root)                        # Append as child so <mt-attr> works when the attribute is on the mt-include tag
                process_node(root)
                
                target.parentNode.replaceChild(root, target)    # Replace the target with root - effectively deleting target and moving it's child up
                return                                          # Root node has already been processed, so we don't need to run the final for loop
                        
                            
            case "mt-glob":                                     # Running a glob - for each file it copies the children and sets the src attribute
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
                return                                          # Root node has already been processed, so we don't need to run the final for loop


            case "mt-attr":                                     # Displays the result of an attribute
                value = closest(target, "name")
                target.parentNode.replaceChild(minidom.Document().createTextNode(value), target)


            case "mt-for":
                start = target.getAttribute("start")
                stop = target.getAttribute("stop")
                step = target.getAttribute("step")
                name = target.getAttribute("name")

                if name == "":
                    name = "i"

                for i in range(start, stop, step):
                    target.setAttribute(name, i);

                    process_node(target)


    # Otherwise, process the children - which might be mt-* elements
    for child in target.childNodes:
        process_node(child)



def processFile(path: str, encoding: str = "utf8") -> str:
    """Processes a single marktemplate file into a static html string"""

    # Process root node
    doc = minidom.parse(path)
    process_node(doc.documentElement)

    # Stringify and return
    return doc.documentElement.toxml()



def processRaw(raw: str) -> str:
    """Processes a parsed raw string into a static html string"""

    # Process root node
    doc = minidom.parseString(raw)
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
    
