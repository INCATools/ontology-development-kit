"""
Generates ODK schema config documentation from the 'project-schema.json'

Schema json doesn't contain field descriptions so extracts those descriptions from 'odk.py' using ast.

Generates the initial (plain) documentation using jsonschema2md library. Then makes documentation more readble through
inlining referred objects and 'allOf' definitions.
"""
import jsonschema2md
import os
import logging
import json
import ast


NESTED_REFERENCE_LIMIT = 3

INLINE_POSTFIX = "_inline"
DEFINITION_PREFIX = "def_"
CROSS_REF_TERM = "Refer to *#/definitions/"
CROSS_REF_TERM_ALT = "Values from *"

logging.basicConfig(level=logging.INFO)

ODK_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../schema/project-schema.json")
ODK_SCHEMA_MD = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../schema/project-schema.md")


def generate_plain_documentation(json_schema, descriptions):
    """
    Generates a plain documentation using jsonschema2md library.

    Returns: Dictionary of element documentations. Key is element name and value is list of documentation lines.
    """
    parser = jsonschema2md.Parser()

    md_lines = parser.parse_schema(json_schema)

    plain_documentation = dict()
    element_lines = []
    element_name = ""

    is_definition = False
    element_path = list()
    prev_indent = 0
    curr_indent = 0
    for line in md_lines:
        if line.startswith("## Definitions"):
            is_definition = True
        elif line.startswith("## Properties"):
            is_definition = False

        line = line.replace("\n", "")

        if line.startswith("- **`"):
            if element_name:
                plain_documentation[element_name] = element_lines
            element_name = get_element_name(is_definition, line)
            element_description = get_element_description(is_definition, element_name, descriptions)
            line = insert_description(line, element_description)
            element_path = [element_name]
            element_lines = [line]
            curr_indent = 0
        elif line and not line.startswith("#") and element_path:
            prev_indent = curr_indent
            curr_indent = len(line) - len(line.lstrip(' '))
            if curr_indent == prev_indent:
                element_path.remove(element_path[-1])
            elif curr_indent <= prev_indent:
                element_path.remove(element_path[-1])
                element_path.remove(element_path[-1])
            inner_element_name = get_element_name(False, line)
            element_description = get_element_description(is_definition, inner_element_name, descriptions, element_name.replace(DEFINITION_PREFIX, ""))
            line = insert_description(line, element_description)
            element_path.append(inner_element_name)
            element_lines.append(line)

    plain_documentation[element_name] = element_lines
    handle_one_of_definitions(json_schema, plain_documentation)
    handle_all_of_definitions(json_schema, plain_documentation, descriptions)

    return plain_documentation


def insert_description(line, description):
    """
    Insert description to the line:
    Parameters:
        line (str): line to modify
        description (str): description to insert
    Returns:
        modified line
    """
    if description and CROSS_REF_TERM not in line:
        parts = line.split("Default:")
        line = parts[0].rstrip() + " " + description
        if len(parts) > 1:
            line += " Default:" + parts[1]
    return line


def get_element_description(is_definition, element_name, descriptions, parent=None):
    """
    Gets element description from the descriptions dictionary.
    Parameters:
        is_definition (bool): identifies if element is part of definitions or parameters section.
        element_name (str): name of the element
        descriptions (dict): dictionary of field descriptions per class.
        parent (str): name of the element's parent
    Returns:
        element description. None, if cannot be found.
    """
    description = None
    if not is_definition:
        if element_name in descriptions["OntologyProject"]:
            description = descriptions["OntologyProject"][element_name]
    else:
        if parent and parent in descriptions and element_name in descriptions[parent]:
            description = descriptions[parent][element_name]

    if description and not str(description).rstrip().endswith('.'):
        description = str(description).rstrip()+'.'

    return description


def get_element_name(is_definition, line):
    """
    Extract element name from jsonschema2md generated documentation line.
    """
    first_occur = line.index("**")
    second_occur = line.index("**", first_occur + 1)
    element_name = line[first_occur + 2:second_occur]
    if "`" in element_name:
        element_name = element_name.replace("`", "").strip()
    if is_definition:
        element_name = DEFINITION_PREFIX + element_name

    return element_name


def handle_one_of_definitions(content, plain_documentation):
    """
    'OneOf' definitions are not handled by the jsonschema2md. Manually adding documentation for these definitions.
    """
    definitions = content["definitions"]
    for key in definitions.keys():
        if "oneOf" in definitions[key]:
            one_of_defs = definitions[key]["oneOf"]
            if "$ref" in one_of_defs[0]:
                element_lines = ["- **`annotations`** *(array)*: One of the followings:"]
                for one_of_item in one_of_defs:
                    element_lines.append("  - **Items**: Refer to *" + one_of_item["$ref"] + "*.")
                plain_documentation[DEFINITION_PREFIX + key] = element_lines


def handle_all_of_definitions(content, plain_documentation, descriptions):
    """
    'AllOf' definitions are not handled by the jsonschema2md. Manually adding documentation for these definitions
    """
    definitions = content["definitions"]
    for key in definitions.keys():
        if "allOf" in definitions[key]:
            all_of_defs = definitions[key]["allOf"]
            element_lines = list()
            for all_of_item in all_of_defs:
                if "$ref" in all_of_item:
                    pass
                    element_lines.append("  - **Items**: Refer to *" + all_of_item["$ref"] + INLINE_POSTFIX + "*.")
                elif "properties" in all_of_item:
                    for prop in all_of_item["properties"]:
                        prop_obj = all_of_item["properties"][prop]
                        if "items" in prop_obj:
                            if "$ref" in prop_obj["items"]:
                                element_lines.append("  - **`" + prop + "`** *(" + prop_obj["type"] + ")*")
                                element_lines.append("  - **Items**: Refer to *" + prop_obj["items"]["$ref"] + "*.")
                            else:
                                if "default" in prop_obj:
                                    default = str(prop_obj["default"])
                                else:
                                    default = ""
                                line = "  - **`" + prop + "`** *(" + prop_obj["type"] + ")*: Default: `" + default + "`."
                                element_description = get_element_description(True, prop, descriptions, key)
                                line = insert_description(line, element_description)
                                element_lines.append(line)
                        else:
                            if "default" in prop_obj:
                                default = str(prop_obj["default"])
                            else:
                                default = ""
                            line = "  - **`" + prop + "`** *(" + prop_obj["type"] + ")*: Default: `" + default + "`."
                            element_description = get_element_description(True, prop, descriptions, key)
                            line = insert_description(line, element_description)
                            element_lines.append(line)

            plain_documentation[DEFINITION_PREFIX + key] = element_lines


def print_element(element, md_out, plain_doc, prefix="", nesting_list=None, in_reference=False):
    """
    Retrieves plain element documentation generated by the jsonschema2md and writes to the document.
    Additionally, expands 'definitions' references to a specified depth (see NESTED_REFERENCE_LIMIT)
    in order to prevent indefinite circular references.
    """
    if nesting_list is None:
        nesting_list = []

    indentation = prefix + ("  " * (len(nesting_list) % 2))
    lines = plain_doc[element]

    # postpone writing references (as last items) to make it more readable
    reference_defs = list()
    reference_elements = dict()
    for count, line in enumerate(lines):
        line = customize_doc_content(line)
        if CROSS_REF_TERM_ALT in line:
            nesting_list.append(element)
            ref_term_start = line.index(CROSS_REF_TERM_ALT) + len(CROSS_REF_TERM_ALT)
            referred_element = line[ref_term_start:len(line) - 2]
            if "- **Items**" not in line:
                md_out.write("%s\n" % (indentation + line.split(CROSS_REF_TERM_ALT)[0].rstrip()))
                # md_out.write("%s\n" % (indentation + line))

            if (DEFINITION_PREFIX + referred_element).replace(INLINE_POSTFIX, "") not in nesting_list:
                if INLINE_POSTFIX in referred_element:
                    # no extra indentation if inline (for allOf definitions)
                    referred_element = referred_element.replace(INLINE_POSTFIX, "")
                    print_element(DEFINITION_PREFIX + referred_element, md_out, plain_doc,
                                  "" if len(nesting_list) == 1 else indentation, nesting_list)
                else:
                    print_element(DEFINITION_PREFIX + referred_element, md_out, plain_doc,
                                  "" if len(nesting_list) == 1 else indentation + "  ", nesting_list)
            else:
                # ellipsis to indicate recursion
                md_out.write("%s\n" % (indentation + " " * (len(line) - len(line.lstrip())) + "  - ..."))
        else:
            if not (element.startswith(DEFINITION_PREFIX) and count == -1 and not in_reference):
                    # and "- **Items**" not in line:
                if not (element.startswith(DEFINITION_PREFIX) and "**`" + element.replace("def_", "") + "`**" in line):
                    md_out.write("%s\n" % (indentation + line))

    for count, reference in enumerate(reference_defs):
        if "**`annotations`** *(list)*: One of the followings:" in reference:
            md_out.write("%s\n" % (indentation + "*Use one of the followings:*"))
        else:
            md_out.write("%s\n" % reference)
        for element in reference_elements[reference]:
            if element not in nesting_list:
                md_out.write("\n")
                print_element(element, md_out, plain_doc,
                              prefix if prefix.startswith(">") else ">" + prefix, nesting_list, in_reference=True)
            else:
                # ellipsis to indicate recursion
                line_content = reference.replace(">", "")
                md_out.write("%s\n" % (indentation + " " * (len(line_content) - len(line_content.lstrip())) + "  - ..."))


def customize_doc_content(line):
    """
    Place content customizations to here. Such as don't display "array", use "list instead"

    Parameters:
        line (str): line to modify
    Returns:
        modified line
    """
    if "*(array)*" in line:
        line = line.replace("*(array)*", "*(list)*")

    if "*(array)*" in line:
        line = line.replace("*(object)*", "*(dict)*")

    if CROSS_REF_TERM in line:
        line = line.replace(CROSS_REF_TERM, CROSS_REF_TERM_ALT)

    return line


def decode_stacked_json(document):
    """
    Json schema is containing multiple schemas and is not a valid json file. Parse it in a different way and get all
    schemas.

    Parameters:
        document: json schema file content as string
    Returns:
        list of json objects extracted from the schema file
    """
    dec = json.JSONDecoder()
    pos = 0
    json_objects = list()
    while not pos == len(document):
        content = str(document[pos:]).strip()
        if content.startswith("}"):
            content = str(document[pos + 1:]).strip()
        if len(content) > 1:
            j, json_len = dec.raw_decode(content)
            json_objects.append(j)
            pos += json_len
        else:
            # sometimes decoder grabs a single final '}'. Ignore it
            break

    return json_objects


def generate_schema_doc(json_schema=ODK_SCHEMA, md_output=ODK_SCHEMA_MD):
    """
    Generates documentation for the given YAML schema. Uses jsonschema2md to generate a plain documentation,
    then decorates generated documentation through inlining referred elements.

    Parameters:
        json_schema: path of the json schema
        md_output: output file path
    """
    with open(json_schema, 'r') as file:
        schema_content = file.read()

    json_objects = decode_stacked_json(schema_content)
    odk_schema = json_objects[0]

    descriptions = extract_field_descriptions()

    logging.info("Target is: " + os.path.abspath(md_output))
    with open(md_output, "w") as md_out:
        md_out.write("\n")
        md_out.write("## %s\n" % "ODK Project Configuration Schema")
        md_out.write("\n")

        plain_doc = generate_plain_documentation(odk_schema, descriptions)
        for element in odk_schema["properties"].keys():
            print_element(element, md_out, plain_doc, nesting_list=[])
            md_out.write("\n\n")


def extract_field_descriptions():
    """
    Extracts field descriptions from the 'odk.py' using ast.

    Returns:
        dictionary of field descriptions per class.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.abspath(os.path.join(current_dir, "odk.py"))
    with open(script_path, 'r') as f:
        fstr = f.read()

    comments = dict()

    script = ast.parse(fstr)
    classes = [n for n in script.body if isinstance(n, ast.ClassDef)]
    for class_ in classes:
        fields = dict()
        assign = None
        for n in class_.body:
            if isinstance(n, ast.AnnAssign):
                if hasattr(n.target, 'id'):
                    assign = n.target.id
            elif isinstance(n, ast.Expr) and assign:
                if hasattr(n.value, 's'):
                    fields[assign] = n.value.s
            else:
                assign = None
        comments[class_.name] = fields

    return comments


generate_schema_doc(ODK_SCHEMA)
