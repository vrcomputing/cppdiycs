#!/usr/bin/python
import os
import argparse
import sys
from lxml import etree

if __name__ == "__main__":

    # command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml', required=True, help='input xml file')
    parser.add_argument('--source', required=False, help='input source files')
    parser.add_argument('--hpp', required=True, help='output *.hpp file')
    parser.add_argument('--cpp', required=True, help='output *.cpp file')
    parser.add_argument('--type', required=False,
                        help='limit output to these types')
    args = parser.parse_args()

    # xml parsing
    tree = etree.parse(args.xml)
    root = tree.getroot()

    # filter for required structs
    query = "Struct[@name = '%s']" % args.type
    structs = root.xpath(query)

    for struct_element in structs:

        # generate header
        header = open(args.hpp, "w")
        header.write('#pragma once\n')
        header.write('#include <%s>\n' % "ostream")
        header.write('#include <%s>\n' % "string")
        header.write('#include <%s>\n' % os.path.basename(args.source))
        header.write('\n')
        header.write('namespace generated\n')
        header.write('{\n')
        header.write('namespace string_util\n')
        header.write('{\n')
        header.write('std::string to_string(const %s& obj);\n' % struct_element.get('name'))
        header.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % struct_element.get('name'))
        header.write('}\n')
        header.write('}\n')
        header.write('\n')
        header.close()

        # generate source
        source = open(args.cpp, "w")
        source.write('#include <%s>\n' % "sstream")
        source.write('#include <%s>\n' % os.path.basename(args.hpp))
        source.write('\n')

        # get all field names
        field_names = []
        for field_element in root.xpath("Field[@context = '%s']" % struct_element.get('id')):
            field_names.append('obj.' + field_element.get('name'))

        # write to_string function
        source.write('std::string %s(const %s& obj)\n' % ('::'.join(
            ['generated', 'string_util', 'to_string']), struct_element.get('name')))
        source.write('{\n')
        source.write('\tstd::ostringstream ss;\n')
        if len(field_names) > 0:
            source.write('\tss << obj;\n')
        source.write('\treturn ss.str();\n')
        source.write('}\n')
        source.write('\n')

        # write << operator
        source.write('std::ostream& %s<<(std::ostream& os, const %s& obj)\n' % ('::'.join(['generated', 'string_util', 'operator']), struct_element.get('name')))
        source.write('{\n')
        if len(field_names) > 0:
            source.write('\tos << %s;\n' % ' << "," << '.join(field_names))
        source.write('\treturn os;\n')
        source.write('}\n')
        source.close()
