import os
import sys
from lxml import etree

# returns the field's type name including namespaces
def get_field_type_name(root, element):
    assert root.tag == 'CastXML', 'invalid root type'
    assert element.tag == 'Field', 'invalid element type'

    element = root.find("*[@id = '%s']" % element.get('type'))
    return get_type_name(root, element)

# returns the type's name including namespaces
def get_type_name(root, element):
    assert root.tag == 'CastXML', 'invalid root type'

    name = [element.get('name')]
    while element is not None and element.get('name') != '::':
        element = root.find("*[@id = '%s']" % element.get('context'))
        if element is not None and element.get('name') != '::':
            name.insert(0, element.get('name'))

    return "::".join(name)

# returns a set of recursively required struct ids
def get_type_field_types(root, element):
    assert root.tag == 'CastXML', 'invalid root type'
    assert element.tag == 'Struct', 'invalid element type'

    fieldids=set({})
    for field in root.xpath("Field[@context = '%s']" % element.get('id')):
        for struct_type in root.xpath("Struct[@id = '%s']" % field.get('type')):
            fieldids=fieldids.union(
                {struct_type.get('id')}, get_type_field_types(root, struct_type))

    return fieldids

# returns a set of file ids for the sources
def get_file_ids_for_sources(root, files):
    assert root.tag == 'CastXML', 'invalid root type'

    fileids=set({})
    for file_element in root.xpath("File"):
        for filename in files:
            if os.path.abspath(file_element.get('name')) == os.path.abspath(filename):
                fileids.add(file_element.get('id'))

    return fileids

# returns a set of all structs for all files
def get_struct_ids_for_files(root, files):
    assert root.tag == 'CastXML', 'invalid root type'

    file_filter=' or '.join(map(lambda v: "@file = '%s'" %
                            v, get_file_ids_for_sources(root, files)))
    query="Struct[%s]" % file_filter
    structs=root.xpath(query)
    structids=set({})
    for struct in structs:
        structids.add(struct.get('id'))
    return structids

# returns all struct elements for the files
def get_structs_for_files(root, files):
    struct_ids = get_struct_ids_for_files(root, files)
    struct_ids_filter = ' or '.join(map(lambda v: "@id = '%s'" % v, struct_ids))
    return root.xpath("Struct[%s]" % struct_ids_filter)    

# returns a set of all structs for all files
def get_enum_ids_for_files(root, files):
    assert root.tag == 'CastXML', 'invalid root type'

    file_filter=' or '.join(map(lambda v: "@file = '%s'" %
                            v, get_file_ids_for_sources(root, files)))
    query="Enumeration[%s]" % file_filter
    structs=root.xpath(query)
    enumids=set({})
    for struct in structs:
        enumids.add(struct.get('id'))
    return enumids

# returns all enum elements for the files
def get_enums_for_files(root, files):
    enum_ids = get_enum_ids_for_files(root, files)
    enum_ids_filter = ' or '.join(map(lambda v: "@id = '%s'" % v, enum_ids))
    return root.xpath("Enumeration[%s]" % enum_ids_filter)

# returns a set of struct id for the types
def get_struct_ids_for_types(root, types):
    assert root.tag == 'CastXML', 'invalid root type'

    query="Struct"
    structs=root.xpath(query)

    structids=set({})
    for struct in structs:
        struct_name=get_type_name(root, struct)
        if struct_name in types:
            structids=structids.union(
                {struct.get('id')}, get_type_field_types(root, struct))

    return structids

# returns a set of all struct ids
def get_struct_ids(root):
    assert root.tag == 'CastXML', 'invalid root type'

    structids=set({})
    for struct in root.xpath("Struct"):
        structids.add(struct.get('id'))

    return structids
