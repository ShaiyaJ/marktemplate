const fs = require("fs");
const path = require("path");


/// Takes a template string and evaluates it with namespace
const evalTemplate = (template, namespace) => {
    with (namespace)
        return eval(`\`${template}\``);
}


/// Processes all child nodes of nodes - recursing if necessary
function processNode(node) {
    for (const target of node.childNodes) {
        switch (target.nodeType) {


            case "mt-raw-include":
                if (target.src)
                    target.outerHTML = fs.readFileSync(target.src, target.encoding ? target.encoding : "utf8");
                break;

                
            case "mt-include":
                if (target.src) {
                    const rawInclude = fs.readFileSync(target.src, target.encoding ? target.encoding : "utf8");

                    // Process new include nodes
                    const parsedInclude = new DOMParser().parseFromString(rawInclude, "application/xml");
                    processNode(parsedInclude);

                    // Replace target node
                    target.innerHTML = serializer.seralizeToString(parsedInclude);
                }
                break;
                

            case "mt-attr":
                target.outerHTML = target.closest(`[${target.textContent.trim()}]`);
                break;


            default:
                processNode(target);
                break;
        }
    }
}


/// Processes a single marktemplate file into a static html file
/// Returns plaintext html
function processFile(path, { encoding = "utf8" } = {}) {

    // Creating the DOM
    const raw = fs.readFileSync(path, encoding);
    const parser = new DOMParser();
    const serializer = new XMLSerializer();
    const DOM = parser.parseFromString(raw, "application/xml");

    processNode(DOM.getRootNode());

    return seralizer.serializeToString(DOM);
}


// Check whether target argument is present
const target = process.argv[2];

if (!target) {
    console.error("Error: no target file provided");
    process.exit(1);
}

// Process file
console.log(processFile(target, "utf8"));
