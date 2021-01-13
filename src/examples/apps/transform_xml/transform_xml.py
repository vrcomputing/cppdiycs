#!/usr/bin/python
import os
import argparse
import sys
from lxml import etree

import cppdiycs as castxml_util

xsd_types = {
    'std::string': 'xs:string',
    'int': 'xs:unsignedInt',
    'float': 'xs:float',
    'double': 'xs:double',
    'unsigned int': 'xs:unsignedInt'
}

xsd_cpp_types = {}

if __name__ == "__main__":

    # command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml', required=True, help='input *.xml file')
    parser.add_argument('--source', nargs='+', required=False, help='input source files')
    parser.add_argument('--xml_hpp', required=True, help='output *.hpp file')
    parser.add_argument('--xml_cpp', required=True, help='output *.cpp file')
    parser.add_argument('--xsd_hpp', required=True, help='output *.hpp file')
    parser.add_argument('--xsd_cpp', required=True, help='output *.cpp file')
    args = parser.parse_args()

    # xml parsing
    tree = etree.parse(args.xml)
    root = tree.getroot()

    # filter for required structs and enums
    structs = castxml_util.get_structs_for_files(root, args.source)
    enums = castxml_util.get_enums_for_files(root, args.source)

    # add c++ type name mapping for xsd
    for struct_node in structs:
        xsd_cpp_types[castxml_util.get_type_name(root, struct_node)] = struct_node.get('name')
    for enum_node in enums:
        xsd_cpp_types[castxml_util.get_type_name(root, enum_node)] = enum_node.get('name')

    # write xsd header file
    with open(args.xsd_hpp, "w") as file:
        file.write('#pragma once\n')
        file.write('#include <%s>\n' % "ostream")
        for source_file in args.source:
            file.write('#include <%s>\n' % os.path.basename(source_file))
        file.write('\n')
        file.write('namespace generated\n')
        file.write('{\n')
        file.write('namespace xsd\n')
        file.write('{\n')
        file.write('namespace root\n')
        file.write('{\n')
        for enum_node in enums:
            type_name_cpp = castxml_util.get_type_name(root, enum_node)
            file.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % castxml_util.get_type_name(root, enum_node))
        for struct_node in structs:
            type_name_cpp = castxml_util.get_type_name(root, struct_node)
            file.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % type_name_cpp)
        file.write('}\n')
        file.write('namespace data\n')
        file.write('{\n')
        for enum_node in enums:
            type_name_cpp = castxml_util.get_type_name(root, enum_node)
            file.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % type_name_cpp)
        for struct_node in structs:
            type_name_cpp = castxml_util.get_type_name(root, struct_node)
            file.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % type_name_cpp)
        file.write('}\n')
        file.write('}\n')
        file.write('}\n')

    # write xsd source file
    with open(args.xsd_cpp, "w") as file:
        file.write('#include <%s>\n' % os.path.basename(args.xsd_hpp))

        for enum_node in enums:
            # generated::xsd::root
            file.write('std::ostream& generated::xsd::root::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, enum_node))
            file.write('{\n')
            file.write('os << R"(<?xml version="1.0" encoding="UTF-8" ?>)";\n')
            file.write('os << R"(<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">)";\n')
            file.write('os << R"(<xs:element name="%s" type="%s"/>)";\n' % (enum_node.get('name'), struct_node.get('name')))
            file.write('os << R"(</xs:schema>)";\n')
            file.write('return os;\n')
            file.write('}\n')
            # generated::xsd::data
            file.write('std::ostream& generated::xsd::data::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, enum_node))
            file.write('{\n')
            file.write('os << R"(<xs:simpleType name="%s">)";\n' % enum_node.get('name'))
            file.write('os << R"(<xs:restriction base="xs:integer">)";\n')  # must be guessed!
            for enum_value_node in enum_node.findall('EnumValue'):
                file.write('os << R"(<!-- %s -->)";\n' % enum_value_node.get('name'))
                file.write('os << R"(<xs:enumeration value="%s"/>)";\n' % enum_value_node.get('init'))
            file.write('os << R"(</xs:restriction>)";\n')
            file.write('os << R"(</xs:simpleType>)";\n')
            file.write('return os;\n')
            file.write('}\n')

        for struct_node in structs:
            # generated::xsd::root
            file.write('std::ostream& generated::xsd::root::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, struct_node))
            file.write('{\n')
            file.write('os << R"(<?xml version="1.0" encoding="UTF-8" ?>)";\n')
            file.write('os << R"(<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">)";\n')
            for field_node in root.xpath("Field[@context = '%s']" % struct_node.get('id')):
                type_name_cpp = castxml_util.get_field_type_name(root, field_node)
                if type_name_cpp in xsd_cpp_types:
                    file.write('data::operator<<(os, decltype(obj.%s){});\n' % field_node.get('name'))
            file.write('data::operator<<(os, obj);\n')
            file.write('os << R"(<xs:element name="%s" type="%s"/>)";\n' % (struct_node.get('name'), struct_node.get('name')))
            file.write('os << R"(</xs:schema>)";\n')
            file.write('return os;\n')
            file.write('}\n')
            # generated::xsd::data
            file.write('std::ostream& generated::xsd::data::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, struct_node))
            file.write('{\n')
            file.write('os << R"(<xs:complexType name="%s">)";\n' % struct_node.get('name'))
            file.write('os << R"(<xs:sequence>)";\n')
            for field_node in root.xpath("Field[@context = '%s']" % struct_node.get('id')):
                type_name_cpp = castxml_util.get_field_type_name(root, field_node)
                type_name_xsd = xsd_types[type_name_cpp] if type_name_cpp in xsd_types else xsd_cpp_types[type_name_cpp]
                file.write('os << R"(<xs:element name="%s" type="%s" minOccurs="1" maxOccurs="1" />)";\n' % (field_node.get('name'), type_name_xsd))
            file.write('os << R"(</xs:sequence>)";\n')
            file.write('os << R"(</xs:complexType>)";\n')
            file.write('return os;\n')
            file.write('}\n')

    # write xml header file 
    with open(args.xml_hpp, "w") as file:
        file.write('#pragma once\n')
        file.write('#include <%s>\n' % "ostream")
        for source_file in args.source:
            file.write('#include <%s>\n' % os.path.basename(source_file))
        file.write('\n')
        file.write('namespace generated\n')
        file.write('{\n')
        file.write('namespace xml\n')
        file.write('{\n')
        file.write('namespace root\n')
        file.write('{\n')
        for struct_node in structs:
            type_name_cpp = castxml_util.get_type_name(root, struct_node)
            file.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % type_name_cpp)
        file.write('}\n')
        file.write('namespace data\n')
        file.write('{\n')
        for struct_node in structs:
            type_name_cpp = castxml_util.get_type_name(root, struct_node)
            file.write('std::ostream& operator<<(std::ostream& os, const %s& obj);\n' % type_name_cpp)
        file.write('}\n')
        file.write('}\n')
        file.write('}\n')
        file.close()

    # write xml source file
    with open(args.xml_cpp, "w") as file:
        file.write('#include <%s>\n' % os.path.basename(args.xml_hpp))
        file.write('\n')
        for struct in structs:
            # generated::xml::data
            file.write('std::ostream& generated::xml::data::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, struct))
            file.write('{\n')
            for field_node in root.xpath("Field[@context='%s']" % struct.get('id')):
                file.write('os << R"(<%s>)" << obj.%s << R"(</%s>)";\n' % (
                    field_node.get('name'), field_node.get('name'), field_node.get('name')))
            file.write('return os;\n')
            file.write('}\n')
            # generated::xml::root
            file.write('std::ostream& generated::xml::root::operator<<(std::ostream& os, const %s& obj)\n' % castxml_util.get_type_name(root, struct))
            file.write('{\n')
            file.write('os << R"(<?xml version="1.0" encoding="UTF-8" ?>)";\n')
            file.write('os << R"(<%s>)";\n' % struct.get('name'))
            file.write('data::operator<<(os, obj);\n')
            file.write('os << R"(</%s>)";\n' % struct.get('name'))
            file.write('return os;\n')
            file.write('}\n')