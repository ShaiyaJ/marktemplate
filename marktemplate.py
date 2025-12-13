from xml.dom import minidom
import sys
import glob


def closest(node, attr):
    """Finds the closest parent that has an attribute"""

    current_attr = node.getAttribute(attr)       
    
    if current_attr != "":
        return current_attr

    return closest(node.parentNode, attr)



def process_node(target: minidom.Node) -> minidom.Node | list[minidom.Node]:
    if target.nodeType == minidom.Node.ELEMENT_NODE:
        match target.tagName:
            case "mt-attr":
                name = target.getAttribute("name")
                value = closest(target, name)

                return minidom.Document().createTextNode(value)

            case "mt-for":
                # Name attribute is optional
                name = target.getAttribute("name")

                if name == "":
                    name = "i"

                # start and stop is mandatory
                start = int( target.getAttribute("start") )
                stop = int( target.getAttribute("stop") )

                # Step attribute is optional
                step = target.getAttribute("step")

                if step == "":
                    step = 1
                else:
                    step = int(step)

                unrolled_children = []

                # For each integer in the range specified
                for i in range(start, stop, step):
                    # Build an array of unaltered childeren
                    clone = target.cloneNode(True)
                    children = clone.childNodes

                    # Set the attribute to i then overwrite it in the children array with the processed varient
                    for j, child in enumerate(children):
                        if child.nodeType == minidom.Node.ELEMENT_NODE:
                            child.setAttribute(name, str(i))
                        children[j] = process_node(child)

                    # Concat to unrolled_children (result array)
                    unrolled_children = unrolled_children + children    # TODO: check for memory issues, allocates a new list?

                return unrolled_children

            case "mt-glob":
                src = target.getAttribute("src")
                files = glob.glob(src)

                # TODO: make recursion a setting?
                # For each file, create a clone of target and set all the children's src attribute to the file path
                children = [] 

                for file in files:
                    clone = target.cloneNode(True)

                    for child in clone.childNodes:
                        if child.nodeType == minidom.Node.ELEMENT_NODE:
                            child.setAttribute("src", file)

                        children.append(process_node(child))

                return children

            case "mt-include":
                src = target.getAttribute("src")

                with open(src, "r") as file:
                    raw = file.read()
                    file.close()

                doc = minidom.parseString(raw)

                return process_node(doc.documentElement).childNodes

            case "mt-raw-include":
                src = target.getAttribute("src")

                with open(src, "r") as file:
                    raw = file.read()
                    file.close()

                return minidom.Document().createTextNode(raw)

            case "mt-text-include":
                src = target.getAttribute("src")

                with open(src, "r") as file:
                    raw = file.read()
                    file.close()

                doc = minidom.parseString(raw)

                return minidom.Document().createTextNode(process_node(doc.documentElement).toxml())

    # Create clone node 
    clone = target.cloneNode(False)

    # For each child, append the processed node
    for child in target.childNodes:
        processed = process_node(child)

        if isinstance(processed, list):             # Tags like for can return multiple children
            for processed_child in processed:
                clone.appendChild(processed_child.cloneNode(True))
        else:
            clone.appendChild(processed.cloneNode(True))

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
HELP = """Marktemplate use:
    marktemplate { [input_path output_path] | [raw] }"""

if __name__ == "__main__":
    if len(sys.argv) == 1:   # There are no arguments
        print(f"Error: no target file/string provided\n{HELP}", file=sys.stderr)
        sys.exit(1)

    elif len(sys.argv) == 2: # Raw text provided
        print(processRaw(sys.argv[1]))
        
    elif len(sys.argv) == 3:
        src = sys.argv[1]
        dest = sys.argv[2]

        with open(dest, "w") as file:
            file.write(processFile(src))
            file.close()

    else:                       # Too many args
        print(f"Error: too many arguments\n{HELP}", file=sys.stderr)
        sys.exit(1)

