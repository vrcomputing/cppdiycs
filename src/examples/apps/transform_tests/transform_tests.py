#!/usr/bin/python
import os
import argparse
import sys
from lxml import etree

if __name__ == "__main__":
	
	# command line parsing
	parser=argparse.ArgumentParser()
	parser.add_argument('--xml', required=True, help='input xml file')
	parser.add_argument('--source', required=True, help='input source file')
	parser.add_argument('--hpp', required=True, help='output *.hpp file')
	parser.add_argument('--cpp', required=True, help='output *.cpp file')
	parser.add_argument('--type', required=True, nargs='+', help='selected type')
	args=parser.parse_args()

	# xml parsing
	tree = etree.parse(args.xml)
	root = tree.getroot()
	
	header_file = open(args.hpp, "w")
	source_file = open(args.cpp, "w")

	# write header file
	header_file.write('#pragma once\n')
	header_file.write('\n')
	
	# write source file
	source_file.write('#include <cassert>\n')
	source_file.write('#include <%s>\n' % os.path.basename(args.source))
	source_file.write('#include <%s>\n' % os.path.basename(args.hpp))
	source_file.write('\n')
	
	query_filter = ' or '.join(map(lambda t: "@name = '%s'" % t, args.type))
	query = "Class[%s]" % query_filter
	classes = root.xpath("Class[%s]" % query_filter)

	for class_element in classes:	
		
		header_file.write('namespace test_suite_%s\n' % class_element.get('name'))
		header_file.write('{\n')

		methods = root.xpath("Method[@context = '%s' and @access = 'public']" % class_element.get('id'))

		# write test case args
		for method_element in methods:
			header_file.write('struct test_case_%s_args\n' % method_element.get('name'))
			header_file.write('{\n');
			for argument_element in method_element.xpath("Argument"):
				argument_type = root.find("FundamentalType[@id = '%s']" % argument_element.get('type')).get('name')
				header_file.write('\t%s %s;\n' % (argument_type, argument_element.get('name')))
			return_type = root.find("FundamentalType[@id = '%s']" % method_element.get('returns')).get('name')
			header_file.write('\t%s expected;\n' % return_type);
			header_file.write('};\n');
		header_file.write('\n');
		
		# write test case declarations
		for method_element in methods:
			header_file.write('bool test_case_%s();\n' % method_element.get('name'))
		header_file.write('bool test_case_all();\n')
		header_file.write('\n')

		# write test case implementation declarations
		header_file.write('// implement these functions\n')
		for method_element in methods:
			header_file.write('test_case_%s_args test_case_%s_get_args();\n' % (method_element.get('name'), method_element.get('name')))
		header_file.write('}\n')
		
		# write forward  declarations
		source_file.write('namespace test_suite_%s\n' % class_element.get('name'))
		source_file.write('{\n');
		for method_element in methods:
			source_file.write('extern test_case_%s_args test_case_%s_get_args();\n' % (method_element.get('name'), method_element.get('name')))
		source_file.write('}\n')
		source_file.write('\n')

		# write test case wrapper
		for method_element in methods:
			source_file.write('bool test_suite_%s::test_case_%s()\n' % (class_element.get('name'), method_element.get('name')))
			source_file.write('{\n');
			source_file.write('\tconst auto args = test_case_%s_get_args();\n' % method_element.get('name'))
			source_file.write('\t%s uut;\n' % class_element.get('name'))
			arguments = []
			for argument_element in method_element.xpath("Argument"):
				arguments.append("args." + argument_element.get('name'))
			source_file.write('\tassert(uut.%s(%s));\n' % (method_element.get('name'), ', '.join(arguments)))
			source_file.write('\treturn true;\n');
			source_file.write('}\n');
			source_file.write('\n');
		
		# write test case all
		source_file.write('bool test_suite_%s::test_case_all()\n' % class_element.get('name'))
		source_file.write('{\n');
		for method_element in methods:
			source_file.write('\tassert(test_case_%s());\n' % method_element.get('name'))
		source_file.write('\treturn true;\n');
		source_file.write('}\n');
		source_file.write('\n');
	
	header_file.close()
	source_file.close()