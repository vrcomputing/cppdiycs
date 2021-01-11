import os
import sys
from lxml import etree

# returns the types name including namespaces
def get_type_name(root, element):
	assert root.tag == 'CastXML', 'invalid root type'

	name = [element.get('name')]

	while element.tag != 'Namespace' and element.get('name') != "::":
		element = root.find("*[@id = '%s']" % element.get('context'))
		name.insert(0, element.get('name'))

	return "::".join(name)

# returns a set of recursively required struct ids
def get_type_field_types(root, element):
	assert root.tag == 'CastXML', 'invalid root type'
	assert element.tag == 'Struct', 'invalid element type'
	
	fieldids = set({})
	for field in root.xpath("Field[@context = '%s']" % element.get('id')):
		for struct_type in root.xpath("Struct[@id = '%s']" % field.get('type')):						
			fieldids = fieldids.union({struct_type.get('id')}, get_type_field_types(root, struct_type))

	return fieldids

# returns a set of file ids for the sources
def get_file_ids_for_sources(root, files):
	assert root.tag == 'CastXML', 'invalid root type'
	
	fileids = set({})
	for file_element in root.xpath("File"):
		for filename in files:
			if os.path.abspath(file_element.get('name')) == os.path.abspath(filename):
				fileids.add(file_element.get('id'))

	return fileids

# returns a set of all structs for all files
def get_struct_ids_for_files(root, files):
	assert root.tag == 'CastXML', 'invalid root type'

	file_filter = ' or '.join(map(lambda v: "@file = '%s'" % v, get_file_ids_for_sources(root, files)))
	query = "Struct[%s]" % file_filter
	structs = root.xpath(query)
	structids = set({})
	for struct in structs:
		structids.add(struct.get('id'))
	return structids

# returns a set of struct id for the types
def get_struct_ids_for_types(root, types):
	assert root.tag == 'CastXML', 'invalid root type'

	query = "Struct"
	structs = root.xpath(query)

	structids = set({})
	for struct in structs: 	
		struct_name = get_type_name(root, struct)			
		if struct_name in types:				
			structids = structids.union({struct.get('id')}, get_type_field_types(root, struct))
	
	return structids

# returns a set of all struct ids
def get_struct_ids(root):
	assert root.tag == 'CastXML', 'invalid root type'

	structids = set({})
	for struct in root.xpath("Struct"): 	
		structids.add(struct.get('id'))

	return structids
