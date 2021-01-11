#!/usr/bin/python
import os
import argparse
import sys
from lxml import etree

import cppdiycs as castxml_util

if __name__ == "__main__":

	# command line parsing
	parser=argparse.ArgumentParser()
	parser.add_argument('--xml', required=True, help='input xml file')
	parser.add_argument('--source', nargs='+', required=False, help='input source files')
	parser.add_argument('--hpp', required=True, help='output *.hpp file')
	parser.add_argument('--cpp', required=True, help='output *.cpp file')
	parser.add_argument('--type', nargs='+', required=False, help='limit output to these types')
	parser.add_argument('--delimiter', required=False, help='delimiter for CSV encoding', default=',')
	args=parser.parse_args()
	
	# xml parsing
	tree = etree.parse(args.xml)
	root = tree.getroot()

	# get all struct ids from all files
	struct_ids_for_files = castxml_util.get_struct_ids(root) if not args.source else castxml_util.get_struct_ids_for_files(root, args.source)
	# get all structs (and recursively required struct ids) fpr the requested types
	struct_ids_for_types = castxml_util.get_struct_ids(root) if not args.type else castxml_util.get_struct_ids_for_types(root, args.type)
	# intersect both id sets to limit the parsing effort
	struct_ids = struct_ids_for_files.intersection(struct_ids_for_types)

	# filter for required structs
	struct_id_filter = ' or '.join(map(lambda v: "@id = '%s'" % v, struct_ids))
	query = "Struct[%s]" % struct_id_filter
	structs = root.xpath(query)

	# generate header
	header = open(args.hpp, "w") 		
	header.write('#pragma once\n')
	header.write('#include <%s>\n' % "ostream")
	for source in args.source:
		header.write('#include <%s>\n' % os.path.basename(source))	
	header.write('\n')
	header.write('namespace csv\n{\n') 

	# create header declarations
	header.write('namespace header\n{\n')
	for struct in structs: 					
		header.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % castxml_util.get_type_name(root, struct))
	header.write('}\n')

	# create data declarations
	header.write('namespace data\n{\n')
	for struct in structs: 					
		header.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % castxml_util.get_type_name(root, struct))
	header.write('}\n')

	header.write('}\n') 
	header.close()

	# generate source
	source = open(args.cpp, "w") 
	source.write('#include <%s>\n' % os.path.basename(args.hpp))
	source.write('\n')

	# create implementations
	for struct in structs: 		
		# find all struct fields
		fields = []
		for field in root.xpath("Field[@context='%s']" % struct.get('id')):			
			fields.append('%s' % field.get('name'))
		
		# create header implementations
		source.write('std::ostream& csv::header::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, struct))
		source.write('{\n')
		if len(fields) > 0:
			source.write('\tos << "%s";\n' % args.delimiter.join(fields));
		source.write('\treturn os;\n');
		source.write('}\n')

		# create data implementations
		source.write('std::ostream& csv::data::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, struct))
		source.write('{\n')
		if len(fields) > 0:
			code = (' << "%s" << ' % args.delimiter).join(map(lambda v: "obj.%s" % v, fields))
			source.write('\tos << %s;\n' % code)
		source.write('\treturn os;\n')
		source.write('}\n')	

	source.close()